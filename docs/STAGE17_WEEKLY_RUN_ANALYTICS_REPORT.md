# Stage 17 — Weekly Run Analytics Report

## What was delivered

Added a reusable per-issue run analytics artifact so each weekly pipeline run leaves behind a concise quality/mix snapshot.

### Changes

1. New script: `scripts/pipeline/run_report.py`
   - Reads:
     - `artifacts/editorial_queue-<issue_id>.json`
     - `artifacts/last_run.json` (if present)
   - Writes:
     - `artifacts/run_report-<issue_id>.md`
   - Includes:
     - Run status (Buttondown result)
     - Total selected items
     - Mix breakdown by:
       - product area
       - source bucket
       - content type
     - Top 5 scored queue items (with links)

2. Pipeline integration: `scripts/pipeline/run_weekly.py`
   - Executes `run_report.py` during weekly run.
   - Adds `artifacts/run_report-<issue_id>.md` to the run summary artifacts list.

3. Queue tracking update
   - `docs/EXECUTION_QUEUE.md` extended with Stage 17 plan + completion record.

## Validation

Executed locally:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
```

Observed:
- `artifacts/run_report-2026-10.md` generated successfully.
- `artifacts/last_run.json` now includes the run report path under `artifacts`.

## Outcome

Stage 17 is complete. Weekly runs now automatically produce an analytics snapshot artifact that improves observability and release confidence without adding manual review steps.
