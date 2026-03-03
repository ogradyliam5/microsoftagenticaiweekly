# Stage 33 — Issue ID Input Validation Guardrail

## Objective
Prevent malformed or impossible `issue_id` overrides from producing ambiguous backfill behavior by adding fail-fast validation in both local CLI and manual GitHub Actions dispatch paths.

## Changes delivered

### 1) Added strict ISO-week issue-id validation in pipeline runner
Updated `scripts/pipeline/run_weekly.py` to validate `--issue-id` with:
- required format: `YYYY-WW`
- week range bounded to the target year's ISO max week (`52` or `53`)

Invalid values now exit immediately with actionable error text before any pipeline steps run.

### 2) Added workflow-dispatch input format guard
Updated `.github/workflows/weekly-editorial.yml` (`Build pipeline args` step) to reject malformed `issue_id` values that do not match `YYYY-WW`, returning a clear error in workflow logs.

### 3) Updated operator runbook
Updated `docs/WEEKLY_PIPELINE.md` with explicit `--issue-id` validation expectations and examples.

## Verification

Local parity checks:

```bash
# valid
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown --skip-source-audit

# invalid format (fails fast)
python3 scripts/pipeline/run_weekly.py --issue-id 2026-W10 --skip-buttondown --skip-source-audit

# impossible week for year (fails fast)
python3 scripts/pipeline/run_weekly.py --issue-id 2026-54 --skip-buttondown --skip-source-audit
```

Expected behavior:
- valid issue ids run normally
- invalid issue ids fail before queue generation with explicit error messaging
