# Stage 30 — Weekly Artifact Enforcement Fail-Fast

## Objective
Upgrade weekly pipeline artifact integrity checks from visibility-only to fail-fast enforcement so partial runs cannot pass silently.

## Changes shipped

### 1) `run_weekly.py` now enforces required artifact completeness by default
- Added `enforce_artifacts` run parameter (default `True`).
- Preserved summary output in `artifacts/last_run.json` and stdout.
- Added `enforce_artifacts` field to run summary for traceability.
- If required artifacts are missing and enforcement is enabled, the script exits non-zero with a clear missing-path list.

### 2) Added local diagnostic opt-out flag
- New CLI option: `--no-enforce-artifacts`
- This keeps summary generation intact but suppresses fail-fast exit for troubleshooting workflows.

### 3) Runbook and queue documentation updated
- Updated `docs/WEEKLY_PIPELINE.md` to reflect default fail-fast behavior and new flag.
- Updated `docs/EXECUTION_QUEUE.md` with Stage 30 plan + completion evidence pointer.

## Verification evidence

Local parity command:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown --skip-source-audit
```

Observed result:
- Command exits successfully when all required artifacts exist.
- `artifacts/last_run.json` includes:
  - `"artifact_check": "ok"`
  - `"missing_artifacts": []`
  - `"enforce_artifacts": true`

## Outcome
Weekly pipeline runs now fail fast on missing required outputs while retaining an explicit local override for diagnostics.