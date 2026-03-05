# Stage 59 — Candidate Audit Ingestability Reason Breakdown

## Goal
Make candidate/rejected feed triage faster by exposing *why* an endpoint is non-ingestable instead of only marking it as non-ingestable.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` with per-feed `ingestability_reason` classification:
  - `machine_ingestable`
  - `no_items`
  - `unsupported_root_tag`
  - `fetch_failed`
- Added summary counters to improve approval/rejection triage:
  - `candidate_add_non_ingestable_no_items`
  - `candidate_add_non_ingestable_unsupported_root`
  - `candidate_reject_now_non_ingestable`
- Updated markdown audit report rows to include `reason: <ingestability_reason>`.
- Updated `docs/WEEKLY_PIPELINE.md` runbook to document reason-level classification and counters.
- Regenerated source audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification evidence
Command:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Observed output:
- `artifacts/source_candidate_audit.json` includes `ingestability_reason` per candidate/reject row plus reason-level summary counters.
- `artifacts/source_candidate_audit.md` includes reason labels per row and summary breakdown lines.

## Dev preview parity
Stage affects pipeline governance script/docs and regenerated audit artifacts only; no frontend template/layout changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
