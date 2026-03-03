# Stage 28 — Weekly Pipeline Governance Parity Hook

## Objective
Ensure weekly pipeline runs always emit current source-governance evidence by executing candidate/rejected feed-health audit automatically and recording status in the run summary.

## Changes delivered
- Updated `scripts/pipeline/run_weekly.py`:
  - Added automatic call to `scripts/pipeline/source_candidate_audit.py`.
  - Added non-blocking status field `source_candidate_audit` in `artifacts/last_run.json` output.
  - Added CLI flag `--skip-source-audit` for offline/local deterministic runs.
  - Added audit artifact paths to run summary artifact list.
- Updated `docs/WEEKLY_PIPELINE.md`:
  - Added source candidate audit step in weekly run order.
  - Documented `--skip-source-audit` local parity option.

## Verification command (local parity)
```bash
python3 scripts/pipeline/run_weekly.py --issue-id 2026-10 --skip-buttondown
```

## Verification result
- Pipeline completed successfully.
- `artifacts/last_run.json` now includes `"source_candidate_audit": "ok"`.
- Source governance artifacts regenerated in the same run:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Guardrails preserved
- Candidate/rejected source audits remain non-promotional: no automatic edits to core approved `sources[]`.
- Failures in source audit are surfaced in run summary status but do not block site artifact generation.

## Evidence
- `scripts/pipeline/run_weekly.py`
- `docs/WEEKLY_PIPELINE.md`
- `artifacts/last_run.json`
- `artifacts/source_candidate_audit.json`
- `artifacts/source_candidate_audit.md`
- `docs/EXECUTION_QUEUE.md`
