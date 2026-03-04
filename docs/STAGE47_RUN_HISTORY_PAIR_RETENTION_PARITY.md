# Stage 47 — Run-History Pair Retention Parity

## Goal
Ensure run-history retention is enforced per run snapshot pair (JSON + markdown), not per individual file, so configured retention capacity is preserved.

## Problem found
`run_weekly.py` previously trimmed `artifacts/run_history/` using a single `last_run-*` file list with `RUN_HISTORY_LIMIT=30`.
Because each run writes two files (`.json` + `.md`), effective run retention could drop to ~15 runs before pruning.

## Changes shipped

1. `scripts/pipeline/run_weekly.py`
   - Added run-history grouping helpers to collect snapshots by base stem.
   - Updated retention pruning to trim by run entry (paired JSON/markdown) rather than raw file count.
   - Extended `run_history` metadata with:
     - `retained_run_count`
     - `orphan_json_count`
     - `orphan_markdown_count`

2. `scripts/pipeline/run_summary_markdown.py`
   - Added run-history section lines for retained run count and orphan diagnostics.

3. `scripts/pipeline/validate_last_run_summary.py`
   - Extended summary contract to require new `run_history` parity fields.

4. `docs/WEEKLY_PIPELINE.md`
   - Updated run summary metadata description to include retained run count + orphan counters.

## Verification

Local parity commands:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected evidence:
- `artifacts/last_run.json` contains `run_history.retained_run_count` and orphan counters.
- `artifacts/last_run.md` includes retained run count + orphan count lines.
- Validator reports pass with the expanded contract.

## Outcome
Run-history retention now keeps up to 30 runs (not 30 files), preserving full forensic depth while surfacing parity drift diagnostics if JSON/markdown snapshots ever diverge.
