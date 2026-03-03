# Stage 34 — Workflow ISO Week Validation Parity

## Goal
Strengthen manual-dispatch issue-id validation in GitHub Actions so invalid ISO weeks fail early (before pipeline invocation), matching `run_weekly.py` guardrail behavior.

## Changes made

1. Updated `.github/workflows/weekly-editorial.yml`:
   - Replaced regex-only guard (`YYYY-WW`) with a Python ISO-week validator.
   - Validation now enforces:
     - required `YYYY-WW` format
     - `week` range bounded by ISO calendar for the selected year (`01..52` or `01..53`).
   - Workflow fails fast with explicit operator-facing error when week is out of range.

2. Updated `docs/WEEKLY_PIPELINE.md`:
   - Documented that manual dispatch validates real ISO week bounds before running `run_weekly.py`.

## Local parity evidence

Static verification:

```bash
grep -n "Invalid issue_id input" .github/workflows/weekly-editorial.yml
```

Expected evidence:
- both invalid format and out-of-range week messages present in workflow input guard block.

## Outcome
Manual dispatch now blocks impossible issue IDs at the workflow boundary, reducing avoidable failed runs and keeping operator feedback immediate.
