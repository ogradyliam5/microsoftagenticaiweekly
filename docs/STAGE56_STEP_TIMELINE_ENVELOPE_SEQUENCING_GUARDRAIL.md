# Stage 56 — Step Timeline Envelope + Sequencing Guardrail

## Goal
Harden `artifacts/last_run.json` contract validation so step telemetry cannot drift outside run bounds or regress in execution order without failing parity checks.

## Changes shipped

1. Extended `scripts/pipeline/validate_last_run_summary.py` step validation signature to include run-level bounds:
   - `_validate_step_results(step_results, run_started_at, run_finished_at)`

2. Added run-envelope checks for step timestamps:
   - Every parsed `started_at` / `finished_at` must be within `[run_started_at, run_finished_at]`.
   - Failed steps with only `finished_at` are still bounded by run-level timestamps.

3. Added sequencing checks across `step_results` order:
   - Step timestamps must be non-decreasing against the previous step `finished_at`.
   - For non-failed steps, `started_at` and `finished_at` must both be `>=` previous step `finished_at`.
   - For failed steps, `finished_at` must be `>=` previous step `finished_at`.

4. Updated weekly runbook guardrail documentation:
   - `docs/WEEKLY_PIPELINE.md` now explicitly calls out run-envelope + sequencing validation parity in CI/local checks.

## Verification

Local parity command:

```bash
python3 scripts/pipeline/validate_last_run_summary.py
```

Result on current artifact:
- Passes with the new run-envelope + sequencing guardrails enabled.

## Outcome
Malformed step telemetry that escapes run bounds or reports out-of-order execution now fails fast in both local and CI validation flows, improving reliability of run diagnostics.
