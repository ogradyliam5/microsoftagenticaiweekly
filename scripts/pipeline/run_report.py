#!/usr/bin/env python3
"""Generate a concise run analytics report from queue + pipeline summary artifacts."""

import argparse
import datetime as dt
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts"


def load_json(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def issue_id_today():
    now = dt.datetime.utcnow()
    y, w, _ = now.isocalendar()
    return f"{y}-{w:02d}"


def fmt_counter(counter: Counter):
    if not counter:
        return "- none"
    return "\n".join(f"- {k}: {v}" for k, v in counter.most_common())


def generate(issue_id: str) -> pathlib.Path:
    queue_path = ART / f"editorial_queue-{issue_id}.json"
    run_path = ART / "last_run.json"

    queue = load_json(queue_path)
    run = load_json(run_path) if run_path.exists() else {}

    items = queue.get("items", [])
    by_area = Counter(i.get("product_area", "unknown") for i in items)
    by_bucket = Counter(i.get("source_mix_bucket", "unknown") for i in items)
    by_type = Counter(i.get("content_type", "unknown") for i in items)

    top_items = sorted(items, key=lambda i: i.get("score_total", 0), reverse=True)[:5]

    lines = [
        f"# Weekly Pipeline Run Report — {issue_id}",
        "",
        f"Generated: {dt.datetime.utcnow().isoformat()}Z",
        "",
        "## Run status",
        f"- Buttondown: {run.get('buttondown', 'unknown')}",
        f"- Queue file: `{queue_path.relative_to(ROOT)}`",
        f"- Last run file: `{run_path.relative_to(ROOT)}`" if run_path.exists() else "- Last run file: not found",
        "",
        "## Output mix",
        f"- Total selected items: {len(items)}",
        "",
        "### By product area",
        fmt_counter(by_area),
        "",
        "### By source bucket",
        fmt_counter(by_bucket),
        "",
        "### By content type",
        fmt_counter(by_type),
        "",
        "## Top scored items",
    ]

    if top_items:
        for idx, item in enumerate(top_items, start=1):
            title = item.get("title", "(untitled)")
            score = item.get("score_total", 0)
            link = item.get("canonical_url") or item.get("url") or ""
            lines.append(f"{idx}. {title} ({score:.4f})")
            if link:
                lines.append(f"   - {link}")
    else:
        lines.append("- none")

    out_path = ART / f"run_report-{issue_id}.md"
    out_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", help="Override ISO week issue id (YYYY-WW).")
    args = ap.parse_args()

    issue_id = args.issue_id or issue_id_today()
    out = generate(issue_id)
    print(json.dumps({"issue_id": issue_id, "report": str(out.relative_to(ROOT))}, indent=2))
