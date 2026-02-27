# Weekly pipeline runbook

## What runs each week

1. `scripts/pipeline/build_queue.py`
   - Reads `data/sources.json`
   - Fetches RSS/Atom sources
   - Normalizes basic metadata
   - Outputs:
     - `artifacts/editorial_queue-<issue_id>.json`
     - `artifacts/editorial_queue-<issue_id>.md`

2. `scripts/pipeline/validate_queue.py`
   - Enforces minimum quality gates:
     - title/canonical URL/published date required
     - summary bullet length caps
     - evidence snippet cap (<=25 words)

3. `scripts/pipeline/generate_issue.py`
   - Converts queue into draft website issue + email draft
   - Outputs:
     - `posts/issue-<issue_id>.md`
     - `drafts/email-<issue_id>.md`

4. `scripts/pipeline/buttondown_draft.py`
   - Creates a Buttondown **draft** (never sends)
   - Records idempotency metadata:
     - `artifacts/buttondown_drafts.json`

## Approval gates (non-negotiable)

- Publishing website post: Liam approval required.
- Sending email: Liam approval required.
- Adding/removing tracked sources: Liam approval required.

## Local/manual run

```bash
python3 scripts/pipeline/run_weekly.py
```

## Sample dry run (Issue 000)

```bash
python3 scripts/pipeline/make_sample_issue000.py
```

## GitHub Actions

Workflow: `.github/workflows/weekly-editorial.yml`

- Scheduled weekly + manual dispatch.
- Uses repo secret: `BUTTONDOWN_API_KEY`.
- Opens PR for approval before any publish/send steps.
