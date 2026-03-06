#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
SECTION_ORDER = ["Power Platform", "M365", "Microsoft Foundry", "Everything else"]


def speaker(item):
    if "Official" in item.get("tags", []):
        return "Microsoft"
    return item.get("publisher") or "Community"


def concise_summary(item):
    title = re.sub(r"\s+", " ", (item.get("title") or "").strip())
    title_l = title.lower()
    publisher = item.get("publisher") or "the author"
    content_type = item.get("content_type", "update")

    what_map = {
        "update": "This post outlines a concrete platform update and what changed in practice.",
        "guide": "This post provides a hands-on guide rather than high-level commentary.",
        "howto": "This post walks through an implementation sequence you can follow.",
        "demo": "This post demonstrates a working approach with practical build details.",
        "build_report": "This post reports lessons from real implementation work rather than theory.",
        "release_notes": "This post captures release-level changes teams need to account for.",
        "analysis": "This post breaks down trade-offs and architectural implications.",
        "news": "This post highlights a noteworthy announcement with delivery impact.",
        "marketing": "This item is announcement-heavy, so focus on the actionable detail.",
        "other": "This post contributes practical context for current Microsoft AI delivery work.",
    }

    if any(k in title_l for k in ["copilot studio", "agent"]):
        why = "It matters because Copilot Studio agent behavior and orchestration choices directly affect reliability, handoff quality, and support load in production."
    elif any(k in title_l for k in ["dataverse", "power apps", "power automate"]):
        why = "It matters because data shape, automation boundaries, and connector decisions here usually determine whether solutions remain maintainable at scale."
    elif any(k in title_l for k in ["foundry", "azure ai", "model", "mcp"]):
        why = "It matters because these choices influence model governance, integration cost, and how quickly teams can move from prototype to controlled operations."
    elif any(k in title_l for k in ["governance", "security", "authentication", "rbac", "policy", "eval"]):
        why = "It matters because governance and control patterns are what prevent high-visibility failures once usage grows beyond pilot scope."
    else:
        why = "It matters because it gives delivery teams concrete decisions to apply now, not just trend commentary."

    custom = (item.get("why_it_matters") or "").strip()
    if custom and "potentially relevant update" not in custom.lower():
        why = custom

    sentence1 = f"{title}"
    sentence2 = what_map.get(content_type, what_map["other"])
    sentence3 = why
    sentence4 = f"Published by {publisher}, this is worth scanning if you are shaping next-sprint implementation choices."
    return " ".join([sentence1, sentence2, sentence3, sentence4])


def narrative_line(item):
    who = speaker(item)
    why = concise_summary(item)
    url = item.get("canonical_url", item.get("url", "#"))
    return f"- **{who}:** {why} [Read source]({url})"


def assign_section(item):
    tags = set(item.get("tags", []))
    if "Power Platform" in tags:
        return "Power Platform"
    if "M365" in tags:
        return "M365"
    if "Foundry" in tags:
        return "Microsoft Foundry"
    return "Everything else"


def section(label, items):
    out = [f"## {label}", ""]
    if not items:
        return out + ["No qualifying items this run.", ""]
    for it in items:
        out += [f"### {it['title']}", narrative_line(it), ""]
    return out


def format_human_date(iso_value):
    try:
        parsed = dt.datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
        return parsed.strftime("%A, %d %B %Y")
    except Exception:
        return dt.datetime.utcnow().strftime("%A, %d %B %Y")


def issue_label(issue_id):
    try:
        y, w = issue_id.split('-', 1)
        week_start = dt.date.fromisocalendar(int(y), int(w), 1)
        return f"Week of {week_start.strftime('%-d %b %Y')}"
    except Exception:
        return f"Edition {issue_id}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    args = ap.parse_args()

    queue_path = ROOT / "artifacts" / f"editorial_queue-{args.issue_id}.json"
    q = json.loads(queue_path.read_text(encoding="utf-8"))
    items = q.get("items", [])

    seen_ids = set()
    unique_items = []
    for item in items:
        key = item.get("id") or item.get("canonical_url") or item.get("url") or item.get("title")
        if key in seen_ids:
            continue
        seen_ids.add(key)
        unique_items.append(item)

    sections = {name: [] for name in SECTION_ORDER}
    for item in unique_items:
        sections[assign_section(item)].append(item)

    publication_date = format_human_date(q.get("generated_at", ""))
    window_start = q.get("window_start_utc", "unknown")
    window_end = q.get("window_end_utc", "unknown")

    label = issue_label(args.issue_id)

    post = [
        f"# Microsoft Agentic AI Weekly — {label}",
        "",
        f"_Published: {publication_date}. Requires human editorial approval before publishing._",
        "",
        "Single weekly digest focused on high-signal agentic AI updates for Microsoft builders.",
        "",
    ]

    for section_name in SECTION_ORDER:
        post += section(section_name, sections[section_name])

    post += [
        "",
        "This edition is a curated weekly digest — use what fits your context.",
        "",
        "If you spot an error or context miss, email [ogradyliam5@gmail.com](mailto:ogradyliam5@gmail.com?subject=Correction%20request).",
        "",
    ]

    email = [
        f"# Microsoft Agentic AI Weekly — {label}",
        "",
        "Draft only. Do not send without Liam approval.",
        f"Published: {publication_date}",
        f"Coverage window (UTC): {window_start} to {window_end} (end exclusive).",
        "",
    ]

    for section_name in SECTION_ORDER:
        email += [f"## {section_name}", ""]
        if not sections[section_name]:
            email += ["No qualifying items this run.", ""]
            continue
        for item in sections[section_name]:
            email.append(f"- **{item['title']}**")
            email.append(f"  {narrative_line(item).lstrip('- ')}")
        email.append("")

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
