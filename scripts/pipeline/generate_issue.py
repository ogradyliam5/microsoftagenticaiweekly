#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]


def lead_phrase(item):
    if "Official" in item.get("tags", []):
        return "Microsoft updated"
    publisher = item.get("publisher") or "A practitioner"
    return f"{publisher} published"


def action_signal(item):
    title = (item.get("title") or "").lower()
    effort = (item.get("effort") or "").lower()
    confidence = (item.get("confidence") or "").lower()

    if any(k in title for k in ["deprecation", "retire", "end of support", "breaking"]):
        return "Adopt"
    if any(k in title for k in ["generally available", "ga", "now available", "released"]):
        return "Pilot"
    if "high" in confidence and "tbd" not in effort:
        return "Pilot"
    return "Watch"


def one_liner(item):
    lead = lead_phrase(item)
    why = item.get("why_it_matters", "Potential impact; verify details before acting.")
    audience = item.get("audience", "Mixed")
    signal = action_signal(item)
    url = item.get("canonical_url", item.get("url", "#"))
    return (
        f"- {lead}: {why} "
        f"**Signal:** {signal} · **For:** {audience} · [Read source]({url})"
    )


def section(items, label, limit=5):
    out = [f"## {label}", ""]
    if not items:
        return out + ["No qualifying items this run.", ""]
    for it in items[:limit]:
        out += [f"### {it['title']}", one_liner(it), ""]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    args = ap.parse_args()

    queue_path = ROOT / "artifacts" / f"editorial_queue-{args.issue_id}.json"
    q = json.loads(queue_path.read_text(encoding="utf-8"))
    items = q.get("items", [])

    pp = [i for i in items if "Power Platform" in i.get("tags", [])]
    m365 = [i for i in items if "M365" in i.get("tags", [])]
    foundry = [i for i in items if "Foundry" in i.get("tags", [])]
    official = [i for i in items if "Official" in i.get("tags", [])]
    community = [i for i in items if "Community" in i.get("tags", [])]

    post = [
        f"# Microsoft Agentic AI Weekly — Issue {args.issue_id}",
        "",
        f"_Generated draft on {dt.datetime.utcnow().date().isoformat()} (requires human editorial approval before publishing)._",
        "",
        "## What changed this week",
        "",
        "Quick scan first; dive into links only where your roadmap is exposed.",
        "",
        "## Top 5 you shouldn’t miss",
        "",
    ]

    if not items:
        post += ["No qualifying items this run.", ""]
    else:
        for idx, it in enumerate(items[:5], start=1):
            post += [f"{idx}. **{it['title']}**", one_liner(it), ""]

    post += section(official, "Official updates")
    post += section(pp, "Power Platform")
    post += section(m365, "M365")
    post += section(foundry, "Foundry")
    post += section(community, "Community picks + creator spotlight")

    post += [
        "## Builder takeaway",
        "",
        "If time is tight, work down Top 5 and only escalate items marked **Pilot** or **Adopt**.",
        "",
        "## Corrections",
        "",
        "If you spot an error or context miss, email [ogradyliam5@gmail.com](mailto:ogradyliam5@gmail.com?subject=Correction%20request).",
        "",
    ]

    email = [
        f"# Microsoft Agentic AI Weekly — Issue {args.issue_id}",
        "",
        "Draft only. Do not send without Liam approval.",
        "",
        "## Top 5 you shouldn’t miss",
        "",
    ]

    if not items:
        email += ["No qualifying items this run."]
    else:
        for it in items[:5]:
            email.append(f"- **{it['title']}**")
            email.append(f"  {one_liner(it).lstrip('- ')}")

    posts = ROOT / "posts"
    drafts = ROOT / "drafts"
    posts.mkdir(exist_ok=True)
    drafts.mkdir(exist_ok=True)

    (posts / f"issue-{args.issue_id}.md").write_text("\n".join(post), encoding="utf-8")
    (drafts / f"email-{args.issue_id}.md").write_text("\n".join(email), encoding="utf-8")
    print(str(posts / f"issue-{args.issue_id}.md"))
    print(str(drafts / f"email-{args.issue_id}.md"))


if __name__ == "__main__":
    main()
