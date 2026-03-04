# Stage 49 — Run-History Index Contract Guardrail

## Goal
Harden `last_run` summary validation so run-history index artifacts are contract-checked, not just presence-checked.

## Problem found
`validate_last_run_summary.py` previously required run-history metadata keys but did not verify that:
- `run_history.index_json` / `run_history.index_markdown` actually existed on disk,
- index payload counts matched `run_history` metadata,
- latest snapshot paths recorded in `run_history` were present inside the generated index.

That gap could allow drift between `artifacts/last_run.json` and `artifacts/run_history/index.json` to pass validation.

## Changes shipped

1. `scripts/pipeline/validate_last_run_summary.py`
   - Added run-history index parity validator that now enforces:
     - index artifact path consistency with `output_artifacts` map,
     - existence of index JSON + markdown files,
     - required index JSON keys (`generated_at`, `retention_limit`, `retained_run_count`, `runs`),
     - retained run-count parity (`retained_run_count == len(runs)`),
     - retained JSON/markdown count parity vs indexed run entries,
     - orphan count parity (`orphan_json_count`, `orphan_markdown_count`),
     - latest run snapshot paths (`run_history.json` + `run_history.markdown`) appear in index entries.

2. `docs/WEEKLY_PIPELINE.md`
   - Updated CI workflow validation note to document run-history index parity checks.

## Verification

Local parity command:

```bash
python3 scripts/pipeline/validate_last_run_summary.py
```

Expected evidence:
- Validator exits 0 when `artifacts/last_run.json` and run-history index artifacts are consistent.
- Validator fails fast with explicit error if index artifacts are missing or count metadata drifts.

## Outcome
Run-summary validation now catches run-history index contract drift early in both local and CI paths, improving release-audit reliability.
