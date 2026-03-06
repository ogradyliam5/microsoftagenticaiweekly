#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SECTION_ORDER = ["Power Platform", "M365", "Microsoft Foundry", "Everything else"]


def speaker(item):
    if "Official" in item.get("tags", []):
        return "Microsoft"
    return item.get("publisher") or "Community"


def concise_summary(item):
    title = " ".join((item.get("title") or "").strip().split())
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

    sentence1 = f"{title}."
    sentence2 = what_map.get(content_type, what_map["other"])
    sentence3 = why
    sentence4 = f"Published by {publisher}, this is worth scanning if you are shaping next-sprint implementation choices."
    return " ".join([sentence1, sentence2, sentence3, sentence4])


def assign_section(item):
    tags = set(item.get("tags", []))
    if "Power Platform" in tags:
        return "Power Platform"
    if "M365" in tags:
        return "M365"
    if "Foundry" in tags:
        return "Microsoft Foundry"
    return "Everything else"


def card(item):
    title = html.escape(item.get("title", "Untitled"))
    by = html.escape(speaker(item))
    summary = html.escape(concise_summary(item))
    url = html.escape(item.get("canonical_url", item.get("url", "#")))
    return f'<article class="rounded-xl border border-slate-800 bg-slate-900 p-5"><h3 class="text-base font-semibold text-white">{title}</h3><p class="mt-2 text-sm leading-6 text-slate-300"><strong class="text-slate-200">{by}:</strong> {summary}</p><p class="mt-3 text-xs text-cyan-300"><a class="hover:text-cyan-200" href="{url}">Read source</a></p></article>'


def section(title, items):
    cards = "\n          ".join(card(i) for i in items) if items else '<p class="text-sm text-slate-400">No qualifying items this run.</p>'
    return f'<section class="mt-8"><h2 class="text-xl font-semibold tracking-tight text-white">{html.escape(title)}</h2><div class="mt-4 grid gap-4">{cards}</div></section>'


def format_human_date(iso_value):
    try:
        parsed = dt.datetime.fromisoformat(iso_value.replace("Z", "+00:00"))
        return parsed.strftime("%A, %d %B %Y")
    except Exception:
        return dt.datetime.utcnow().strftime("%A, %d %B %Y")


def issue_label(issue_id, generated_at):
    try:
        year, week = issue_id.split("-", 1)
        year_i = int(year)
        week_i = int(week)
        week_start = dt.date.fromisocalendar(year_i, week_i, 1)
        return f"Week of {week_start.strftime('%-d %b %Y')}"
    except Exception:
        return f"Edition {issue_id}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--issue-id", required=True)
    args = ap.parse_args()

    q = json.loads((ROOT / "artifacts" / f"editorial_queue-{args.issue_id}.json").read_text(encoding="utf-8"))
    items = q.get("items", [])

    unique_items = []
    seen_ids = set()
    for item in items:
        key = item.get("id") or item.get("canonical_url") or item.get("url") or item.get("title")
        if key in seen_ids:
            continue
        seen_ids.add(key)
        unique_items.append(item)

    sections = {name: [] for name in SECTION_ORDER}
    for item in unique_items:
        sections[assign_section(item)].append(item)

    window_start = html.escape(q.get("window_start_utc", "unknown"))
    window_end = html.escape(q.get("window_end_utc", "unknown"))
    publication_date = html.escape(format_human_date(q.get("generated_at", "")))
    label = html.escape(issue_label(args.issue_id, q.get("generated_at", "")))

    section_html = "\n\n        ".join(section(name, sections[name]) for name in SECTION_ORDER)

    body = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>
    (function () {{
      var key = 'maiw-theme';
      var theme = 'dark';
      try {{
        var stored = localStorage.getItem(key);
        if (stored === 'light' || stored === 'dark') {{
          theme = stored;
        }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
          theme = 'dark';
        }} else {{
          theme = 'light';
        }}
      }} catch (e) {{}}
      var root = document.documentElement;
      root.setAttribute('data-theme', theme);
      root.classList.remove('theme-dark', 'theme-light');
      root.classList.add(theme === 'dark' ? 'theme-dark' : 'theme-light');
      root.style.colorScheme = theme;
    }})();
  </script>
  <title>{label} — Microsoft Agentic AI Weekly</title>
  <link rel="stylesheet" href="../assets/legacy.css?v=20260305" />
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="../index.html">Microsoft Agentic AI Weekly</a>
      <nav class="nav">
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle color mode">🌙 Dark</button>
        <a href="../index.html">Home</a>
        <a href="../archive.html">Archive</a>
        <a href="../about.html">Methodology</a>
      </nav>
    </div>
  </header>
  <main>
    <div class="container content-shell">
      <article class="panel">
        <p class="kicker">{label}</p>
        <h1>Microsoft Agentic AI Weekly</h1>
        <p class="meta">Published: {publication_date}</p>
        <p class="meta">Coverage window (UTC): {window_start} to {window_end} (end exclusive).</p>

        {section_html}

        <p>This edition is a curated weekly digest — use what fits your context.</p>
      </article>
    </div>
  </main>
  <script src="../assets/theme.js?v=20260304"></script>
</body>
</html>
'''

    out = ROOT / "posts" / f"issue-{args.issue_id}.html"
    out.write_text(body, encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
