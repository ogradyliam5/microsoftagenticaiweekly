# Stage 46 — Run History Collision-Proof Snapshots

## Goal
Prevent run-history snapshot overwrites when multiple weekly runs for the same `issue_id` finish within the same second.

## Changes shipped

1. `scripts/pipeline/run_weekly.py`
   - Hardened `_write_run_history_snapshot()` with collision-safe naming.
   - Base snapshot name remains:
     - `last_run-<issue_id>-<timestamp>.json`
     - `last_run-<issue_id>-<timestamp>.md`
   - If a same-second snapshot already exists, appends deterministic numeric suffixes:
     - `...-01`, `...-02`, etc.
   - Extended `run_history` metadata in `artifacts/last_run.json` with:
     - `retained_markdown_count`

2. `scripts/pipeline/run_summary_markdown.py`
   - Updated run-history section labels for clarity.
   - Surfaces both retained JSON and retained markdown snapshot counts.

3. `scripts/pipeline/validate_last_run_summary.py`
   - Extended summary contract validation to require `run_history.retained_markdown_count` when `run_history` is present.

4. `docs/WEEKLY_PIPELINE.md`
   - Documented collision-safe snapshot suffix behavior and expanded run-history metadata description.

## Verification

Local parity commands:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected result:
- `artifacts/last_run.json` and `artifacts/last_run.md` regenerate successfully.
- `artifacts/run_history/` receives a non-overwriting snapshot for each run.
- Validator prints:
  - `last_run summary validation passed: .../artifacts/last_run.json`

## Outcome

Run-history retention is now resilient to same-second run collisions, preserving full forensic history for repeated local/CI reruns without snapshot loss.
