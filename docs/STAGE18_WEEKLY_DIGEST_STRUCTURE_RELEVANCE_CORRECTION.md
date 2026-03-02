# Stage 18 — Weekly Digest Structure + Relevance Correction

## Scope delivered

Implemented and verified all requested constraints in the weekly pipeline and regenerated latest issue artifacts.

1. Exactly 4 sections only in issue markdown: **Power Platform, M365, Microsoft Foundry, Everything else**.
2. Global dedupe across sections (single placement per item).
3. Full human-readable publication date in issue header.
4. Removed disliked labels/phrases from latest outputs (`Adopt/Pilot/Watch`, `best fit`, `what to do next`, `keep an eye on`).
5. Creator names used explicitly in item lines.
6. Tightened AI relevance filtering to exclude non-AI items where possible.

## Code changes

- `scripts/pipeline/build_queue.py`
  - Increased `RELEVANCE_MIN_SCORE` from `0.45` to `0.60`.
  - Reworked `relevance_score(...)` with a hard AI-signal gate:
    - Requires explicit AI/agent signal terms to score above 0.
    - Uses stronger off-topic penalties.
    - Further down-ranks marketing/news content.

- `scripts/pipeline/generate_issue.py`
  - Keeps only the 4 required section headers in generated issue markdown.
  - Preserves full human-readable publication date in header.
  - Retains global dedupe logic before section assignment.

- `scripts/pipeline/render_issue_html.py`
  - HTML output now aligns with 4-section structure expectation (no extra section heading beyond the 4 required product sections).

## Regenerated latest artifacts (Issue 2026-10)

- `artifacts/editorial_queue-2026-10.json`
- `artifacts/editorial_queue-2026-10.md`
- `artifacts/run_report-2026-10.md`
- `artifacts/last_run.json`
- `posts/issue-2026-10.md`
- `posts/issue-2026-10.html`
- `drafts/email-2026-10.md`

## Validation notes

- Issue markdown now has exactly these `##` sections:
  - Power Platform
  - M365
  - Microsoft Foundry
  - Everything else
- No duplicate item titles across sections in latest issue.
- Publication header includes full date format (`Monday, 02 March 2026`).
- Latest outputs do not contain the disallowed phrasing set.
- Filter tightening reduced included queue size from 8 to 3 for this run, removing weak/non-AI items.
