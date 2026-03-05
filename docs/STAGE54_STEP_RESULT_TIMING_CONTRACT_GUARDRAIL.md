# Stage 54 — Step-Result Timing Contract Guardrail

## What changed

- Extended `scripts/pipeline/validate_last_run_summary.py` with `_validate_step_results(...)`.
- Added explicit validation for every `step_results[]` entry:
  - required keys (`name`, `status`, `command`, `started_at`, `finished_at`, `duration_seconds`)
  - failed-step tolerance (`failed_exit_*` may have `started_at`/`duration_seconds` null)
  - non-failed strictness (UTC timestamps required, `finished_at >= started_at`, non-negative numeric duration)
- Updated `docs/WEEKLY_PIPELINE.md` to document step-result timing contract checks in CI parity notes.

## Why

Run summaries are now used for operator triage and CI diagnostics. If step timing fields become malformed, troubleshooting quality drops fast. This guardrail fails fast on bad timing payloads before promotion decisions rely on them.

## Verification

Local parity command:

```bash
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected result:

- `last_run summary validation passed: artifacts/last_run.json`

This confirms the tightened timing contract validates current run output successfully.
