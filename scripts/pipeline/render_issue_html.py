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


def sunday_night_publication(issue_id, fallback_iso_value=""):
    try:
        year, week = issue_id.split("-", 1)
        monday = dt.date.fromisocalendar(int(year), int(week), 1)
        sunday = monday + dt.timedelta(days=6)
        return f"Sunday night, {sunday.strftime('%d %B %Y')}"
    except Exception:
        return f"Sunday night, {format_human_date(fallback_iso_value)}"


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

    publication_date = html.escape(sunday_night_publication(args.issue_id, q.get("generated_at", "")))
    label = html.escape(issue_label(args.issue_id, q.get("generated_at", "")))

    section_html = "\n        ".join(section(name, sections[name]) for name in SECTION_ORDER)

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
  <link rel="stylesheet" href="../assets/styles.css?v=20260306" />
  <link rel="stylesheet" href="../assets/theme-shared.css?v=20260306" />
</head>
<body class="min-h-screen bg-slate-950 text-slate-100">
<header class="sticky top-0 z-20 border-b border-slate-800/90 bg-slate-950/90 backdrop-blur"><div class="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8"><a class="text-sm font-semibold uppercase tracking-[0.15em] text-slate-200" href="../index.html">Microsoft Agentic AI Weekly</a><nav class="flex items-center gap-4 text-sm text-slate-400"><button class="theme-toggle" type="button" data-theme-toggle aria-label="Toggle color mode">🌙 Dark</button><a class="hover:text-white" href="../posts/issue-{args.issue_id}.html">Latest edition</a><a class="hover:text-white" href="../archive.html">Archive</a><a class="hover:text-white" href="../about.html">Methodology</a></nav></div></header>
<main class="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 sm:py-10 lg:px-8 lg:py-12">
  <section class="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl shadow-slate-950/50 sm:p-8">
    <p class="text-xs font-semibold uppercase tracking-[0.18em] text-cyan-300">{label}</p>
    <h1 class="mt-3 text-3xl font-bold tracking-tight text-white">Microsoft Agentic AI Weekly</h1>
    <p class="mt-3 text-sm uppercase tracking-[0.14em] text-slate-400">Published: {publication_date}</p>

        {section_html}

    <p class="mt-8 text-sm text-slate-300">This edition is a curated weekly digest — use what fits your context.</p>
  </section>
</main>
<footer class="border-t border-slate-800 py-5"><div class="mx-auto flex w-full max-w-6xl items-center justify-between gap-3 px-4 text-xs text-slate-500 sm:px-6 lg:px-8"><span>© 2026 Microsoft Agentic AI Weekly · Source-first methodology in <a class="hover:text-slate-300" href="../about.html">About</a></span><a class="hover:text-slate-300" href="../feed.xml">RSS</a></div></footer>
<script src="../assets/theme.js?v=20260306"></script>
</body>
</html>
'''

    out = ROOT / "posts" / f"issue-{args.issue_id}.html"
    out.write_text(body, encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
