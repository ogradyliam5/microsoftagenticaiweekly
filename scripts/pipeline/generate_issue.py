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
        "update": "It reports a product or platform change with implementation impact this week.",
        "guide": "It is a practical guide with steps teams can apply immediately.",
        "howto": "It walks through a how-to flow teams can reproduce with minimal setup guesswork.",
        "demo": "It shows a live build path rather than abstract recommendations.",
        "build_report": "It captures real build outcomes, including what worked and what needed adjustment.",
        "release_notes": "It summarizes release-level deltas likely to affect delivery plans and governance checks.",
        "analysis": "It analyzes trade-offs and likely downstream architecture consequences.",
        "news": "It flags a notable announcement and translates why it should matter to delivery teams.",
        "marketing": "It is announcement-heavy, so the practical signal is extracted and condensed here.",
        "other": "It still adds practical context for current Microsoft AI implementation work.",
    }

    if any(k in title_l for k in ["copilot studio", "agent"]):
        angle = "Use it to tighten agent orchestration decisions, handoff behavior, and support readiness before broad rollout."
    elif any(k in title_l for k in ["dataverse", "power apps", "power automate"]):
        angle = "Use it to validate data/automation boundaries now, because these choices usually decide long-term maintainability."
    elif any(k in title_l for k in ["foundry", "azure ai", "model", "mcp"]):
        angle = "Use it to de-risk model and integration choices that affect governance effort and time-to-production."
    elif any(k in title_l for k in ["governance", "security", "authentication", "rbac", "policy", "eval"]):
        angle = "Use it to harden control points early, before pilot shortcuts become production incidents."
    else:
        angle = "Use it to inform next-sprint priorities with specific, build-relevant context rather than trend chatter."

    custom = (item.get("why_it_matters") or "").strip()
    if custom and "potentially relevant update" not in custom.lower():
        angle = custom

    sentence1 = f"{title}."
    sentence2 = what_map.get(content_type, what_map["other"])
    sentence3 = angle
    sentence4 = f"Source: {publisher}."
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


def sunday_night_publication(issue_id, fallback_iso_value=""):
    try:
        year, week = issue_id.split("-", 1)
        monday = dt.date.fromisocalendar(int(year), int(week), 1)
        sunday = monday + dt.timedelta(days=6)
        return f"Sunday night, {sunday.strftime('%d %B %Y')}"
    except Exception:
        return f"Sunday night, {format_human_date(fallback_iso_value)}"


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

    publication_date = sunday_night_publication(args.issue_id, q.get("generated_at", ""))
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
