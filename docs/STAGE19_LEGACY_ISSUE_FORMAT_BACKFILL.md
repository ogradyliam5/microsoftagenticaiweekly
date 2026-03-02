# Stage 19 — Legacy Issue Format Backfill

## Objective
Backfill older generated issue artifacts that still contained deprecated framing and ensure they match the current Stage 18 digest structure.

## Work completed
- Regenerated markdown + email drafts + HTML for:
  - `issue-000`
  - `issue-2026-09`
- Confirmed both issues now use:
  - 4-section digest (`Power Platform`, `M365`, `Microsoft Foundry`, `Everything else`)
  - one-pass deduped content flow from the current renderer
  - human-readable publication metadata line
  - no `Adopt/Pilot/Watch` builder takeaway block

## Commands run
```bash
python3 scripts/pipeline/generate_issue.py --issue-id 000
python3 scripts/pipeline/render_issue_html.py --issue-id 000
python3 scripts/pipeline/generate_issue.py --issue-id 2026-09
python3 scripts/pipeline/render_issue_html.py --issue-id 2026-09
```

## Artifacts updated
- `posts/issue-000.md`
- `posts/issue-000.html`
- `drafts/email-000.md`
- `posts/issue-2026-09.md`
- `posts/issue-2026-09.html`
- `drafts/email-2026-09.md`
- `docs/EXECUTION_QUEUE.md`
