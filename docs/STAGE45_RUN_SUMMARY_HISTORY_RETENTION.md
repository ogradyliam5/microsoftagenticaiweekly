# Stage 45 — Run Summary History Retention

## Goal
Persist timestamped weekly run summary snapshots for longitudinal debugging while keeping `artifacts/last_run.*` as canonical latest pointers.

## Changes shipped

1. `scripts/pipeline/run_weekly.py`
   - Added bounded run-history retention at `artifacts/run_history/`.
   - After each successful summary render, copies `artifacts/last_run.json` and `artifacts/last_run.md` to timestamped snapshot files:
     - `artifacts/run_history/last_run-<issue_id>-<timestamp>.json`
     - `artifacts/run_history/last_run-<issue_id>-<timestamp>.md`
   - Enforces retention cap of latest 30 runs (oldest snapshots trimmed automatically).
   - Adds `run_history` metadata into `artifacts/last_run.json` for traceability.

2. `scripts/pipeline/run_summary_markdown.py`
   - Added `Run history snapshot` section so `artifacts/last_run.md` surfaces snapshot paths and retention metadata.

3. `scripts/pipeline/validate_last_run_summary.py`
   - Extended summary contract to require `run_history`.
   - Validates `run_history` is either `null` or contains required keys:
     - `json`, `markdown`, `retention_limit`, `retained_json_count`.

4. `docs/WEEKLY_PIPELINE.md`
   - Documented run-history retention behavior and `run_history` contract field.

## Verification

Local parity commands:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected result:
- `artifacts/last_run.json` and `artifacts/last_run.md` are regenerated.
- Timestamped snapshots are written under `artifacts/run_history/`.
- Validator prints `last_run summary validation passed: .../artifacts/last_run.json`.

## Outcome

Each weekly run now leaves durable, bounded history snapshots for trend/debug analysis without sacrificing deterministic latest-summary pointers used by CI and local operator workflows.
