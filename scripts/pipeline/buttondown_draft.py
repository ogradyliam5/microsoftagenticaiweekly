#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
STATE = ROOT / "artifacts" / "buttondown_drafts.json"


def log(level, message, **fields):
    event = {"level": level, "message": message}
    event.update(fields)
    print(json.dumps(event, ensure_ascii=False))


def read_http_error(err):
    body = ""
    try:
        body = err.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""

    parsed = None
    if body:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None

    return {
        "code": getattr(err, "code", None),
        "reason": getattr(err, "reason", ""),
        "body": body,
        "json": parsed,
    }


def api(method, path, token, payload=None):
    url = f"https://api.buttondown.email/v1{path}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Token {token}")
    req.add_header("Accept", "application/json")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        txt = r.read().decode("utf-8")
        return json.loads(txt) if txt else {}


def load_state():
    if not STATE.exists():
        return {}
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state):
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-file", required=True)
    args = ap.parse_args()

    token = os.getenv("BUTTONDOWN_API_KEY", "").strip()
    if not token:
        log("warn", "BUTTONDOWN_API_KEY missing; skipping draft sync", issue_id=args.issue_id)
        return

    body = pathlib.Path(args.body_file).read_text(encoding="utf-8")

    create_payload = {
        "subject": args.subject,
        "body": body,
    }
    update_payload = {
        "subject": args.subject,
        "body": body,
    }

    state = load_state()
    existing_draft_id = str(state.get(args.issue_id, {}).get("draft_id", "")).strip()

    created_or_updated = None
    action = "created"

    try:
        if existing_draft_id:
            try:
                created_or_updated = api("PATCH", f"/emails/{existing_draft_id}", token, update_payload)
                action = "updated"
            except urllib.error.HTTPError as e:
                detail = read_http_error(e)

                if e.code == 404:
                    log(
                        "warn",
                        "Buttondown draft id not found; recreating",
                        issue_id=args.issue_id,
                        draft_id=existing_draft_id,
                    )
                    created_or_updated = api("POST", "/emails", token, create_payload)
                    action = "recreated"
                elif e.code == 422:
                    log(
                        "warn",
                        "Buttondown rejected PATCH (422); creating replacement draft",
                        issue_id=args.issue_id,
                        draft_id=existing_draft_id,
                        http_code=detail["code"],
                        response=detail["json"] if detail["json"] is not None else detail["body"][:400],
                    )
                    created_or_updated = api("POST", "/emails", token, create_payload)
                    action = "recreated_after_422"
                else:
                    raise
        else:
            created_or_updated = api("POST", "/emails", token, create_payload)
    except urllib.error.HTTPError as e:
        detail = read_http_error(e)
        log(
            "error",
            "Buttondown draft sync failed",
            issue_id=args.issue_id,
            existing_draft_id=existing_draft_id,
            http_code=detail["code"],
            reason=str(detail["reason"]),
            response=detail["json"] if detail["json"] is not None else detail["body"][:600],
            action="continuing_without_email_draft",
        )
        return
    except Exception as e:
        log(
            "error",
            "Unexpected Buttondown draft sync error",
            issue_id=args.issue_id,
            existing_draft_id=existing_draft_id,
            error=str(e),
            action="continuing_without_email_draft",
        )
        return

    state[args.issue_id] = {
        "draft_id": created_or_updated.get("id"),
        "absolute_url": created_or_updated.get("absolute_url", ""),
        "updated_at": dt.datetime.utcnow().isoformat() + "Z",
        "action": action,
    }
    save_state(state)
    log("info", "Buttondown draft sync complete", issue_id=args.issue_id, **state[args.issue_id])


if __name__ == "__main__":
    main()
