# Stage 53 — Latest Snapshot Filename Parity Guardrail

## Goal
Harden `artifacts/last_run.json` contract validation so latest run-history pointers cannot silently drift when JSON/markdown snapshot filenames no longer align.

## Changes shipped

1. **Extended validator with snapshot filename parser**
   - Updated `scripts/pipeline/validate_last_run_summary.py` with strict run-history snapshot filename parsing:
     - Required format: `last_run-<issue_id>-<YYYYMMDDTHHMMSSZ>[-NN].(json|md)`
   - Added fail-fast validation for latest snapshot pointers:
     - `run_history.json` must reference `.json`
     - `run_history.markdown` must reference `.md`
     - Both must carry the same `issue_id`
     - Both must carry the same timestamp segment
     - Both must carry the same collision suffix (`-NN`, if present)

2. **Added timestamp bound checks for latest snapshot pointer**
   - Enforced parsed latest snapshot timestamp must be <= summary `run_finished_at`
   - Enforced parsed latest snapshot timestamp must be <= summary `generated_at`

3. **Runbook parity note updated**
   - Updated `docs/WEEKLY_PIPELINE.md` to include latest snapshot filename timestamp/suffix parity checks in CI/local contract validation scope.

## Verification evidence

Local parity command:

```bash
python3 scripts/pipeline/validate_last_run_summary.py
```

Result:
- `last_run summary validation passed: /home/liam_vm/.openclaw/workspace/microsoftagenticaiweekly/artifacts/last_run.json`

## Outcome
Latest run-history pointers now have deterministic filename-level parity checks, closing a drift gap where index and existence checks could pass while JSON/markdown latest pointers encoded mismatched issue/time/suffix metadata.
