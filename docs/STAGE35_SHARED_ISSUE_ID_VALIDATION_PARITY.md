# Stage 35 — Shared Issue-ID Validation Parity

## Objective
Eliminate duplicated `issue_id` validation logic between the local weekly runner and GitHub Actions manual dispatch path.

## Changes shipped
- Added shared validator module: `scripts/pipeline/issue_id_guard.py`
  - Enforces strict `YYYY-WW` format.
  - Enforces real ISO-week bounds per year (`01..52/53`).
- Updated `scripts/pipeline/run_weekly.py` to use the shared validator.
- Updated `.github/workflows/weekly-editorial.yml` manual-dispatch input validation to import and use the same shared validator.
- Updated `docs/WEEKLY_PIPELINE.md` to document shared-validator parity.

## Verification evidence
Local parity checks:

```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-53 --skip-buttondown --skip-source-audit --no-enforce-artifacts
# exits non-zero with invalid issue-id message (2026 has max ISO week 52)

python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown --skip-source-audit
# succeeds and writes artifacts/last_run.json
```

Workflow parity:
- Manual dispatch input validation step now imports `issue_id_guard.py` before building pipeline args.
- Invalid manual `issue_id` values fail fast with shared error semantics.
