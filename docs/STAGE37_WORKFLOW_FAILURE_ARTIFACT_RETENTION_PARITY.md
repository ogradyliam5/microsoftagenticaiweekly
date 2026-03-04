# Stage 37 — Workflow Failure Artifact Retention Parity

## Objective
Preserve weekly pipeline diagnostics in GitHub Actions even when `run_weekly.py` exits non-zero.

## Changes shipped
- Updated `.github/workflows/weekly-editorial.yml` artifact upload step:
  - `if` now uses `always() && steps.london_gate.outputs.run_pipeline == 'true'`
  - Added `if-no-files-found: warn`
- Updated `docs/WEEKLY_PIPELINE.md` to document failure-path artifact retention behavior.
- Updated `.gitignore` to ignore Python bytecode/cache artifacts (`__pycache__/`, `*.pyc`) so local regression runs do not pollute repo status.
- Updated `docs/EXECUTION_QUEUE.md` with Stage 37 plan + completion log entry.

## Verification evidence
- Workflow logic now guarantees artifact upload step execution after pipeline failure paths, while preserving the existing London schedule/manual gate.
- Local diff confirms only workflow/runbook/queue documentation updates for this stage.

## Outcome
CI now keeps run artifacts available for post-failure investigation instead of dropping diagnostic context when pipeline execution fails early.
