# Stage 44 — Run Summary Contract Validation Guardrail

## Goal
Add a deterministic validator for `artifacts/last_run.json` so CI/local runs fail fast when run-summary structure or artifact consistency drifts.

## Changes shipped

1. `scripts/pipeline/validate_last_run_summary.py`
   - Added a reusable contract validator for `artifacts/last_run.json`.
   - Enforces required top-level keys (`pipeline_status`, telemetry, artifact maps, etc.).
   - Verifies required artifact paths are represented in `artifact_checks`.
   - Verifies `missing_artifacts` and `artifact_check` are consistent with `artifact_checks`.
   - Verifies `output_artifact_checks` labels/path mappings align to `output_artifacts`.

2. `.github/workflows/weekly-editorial.yml`
   - Added `Validate run summary contract` step that executes:
     - `python3 scripts/pipeline/validate_last_run_summary.py`
   - Runs on the same `always()` path used for CI summary publishing so summary drift is surfaced immediately.

3. `docs/WEEKLY_PIPELINE.md`
   - Documented workflow validation behavior and local parity command.

## Verification

Local parity commands:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected result:
- Validator prints `last_run summary validation passed: .../artifacts/last_run.json`
- Non-zero exit if summary schema/consistency drifts.

## Outcome

Run-summary diagnostics are now guarded by an explicit contract check, improving CI confidence and preventing silent drift in weekly-run telemetry/evidence artifacts.
