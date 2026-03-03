# Stage 29 — Weekly Output Artifact Integrity Guardrail

## Objective
Add a guardrail in weekly pipeline summaries so operators can immediately see whether expected artifacts were actually produced.

## Changes shipped

### 1) `run_weekly.py` now verifies artifact existence
- Added artifact verification before writing `artifacts/last_run.json`.
- Added summary fields:
  - `artifact_check`: `ok` or `missing_artifacts`
  - `missing_artifacts`: list of missing output paths
  - `artifact_checks`: map of `path -> bool`
- Source-audit artifacts are only included in expected artifact checks when source audit is not skipped.

### 2) Pipeline runbook updated
- `docs/WEEKLY_PIPELINE.md` now documents weekly summary integrity checks and the new run summary fields.

### 3) Execution queue updated
- Added Stage 29 plan and completion log entry in `docs/EXECUTION_QUEUE.md`.

## Verification evidence

Local parity command:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
```

Observed result (excerpt):
- `"artifact_check": "ok"`
- `"missing_artifacts": []`
- `"artifact_checks"` includes all expected queue/issue/report/source-audit outputs with `true` values.

## Outcome
Weekly runs now self-report output integrity in one place (`artifacts/last_run.json`), reducing silent partial-run risk before release/promotion decisions.
