# Stage 64 — Candidate Audit Reason-Bucket Queue Parity

## Goal
Make source-candidate audit action queues more operator-friendly by (1) grouping non-ingestable IDs by ingestability reason and (2) enforcing deterministic ID ordering so successive runs produce stable diffs.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` summary output with:
  - `candidate_add_non_ingestable_ids_by_reason`
  - `candidate_reject_non_ingestable_ids_by_reason`
- Added deterministic sorting/unique normalization for all actionable ID queues in summary output:
  - `candidate_add_promotion_candidate_ids`
  - `candidate_add_non_ingestable_ids`
  - `candidate_add_failed_ids`
  - `candidate_reject_revival_candidate_ids`
  - `candidate_reject_non_ingestable_ids`
  - `candidate_reject_still_blocked_ids`
- Updated markdown report rendering to print per-reason non-ingestable ID buckets for both candidate-add and candidate-reject cohorts.
- Updated `docs/WEEKLY_PIPELINE.md` to document reason-bucketed queues and deterministic ordering guarantees.
- Regenerated source audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification
```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Command completed successfully and rewrote both audit artifacts with the new reason-bucketed queues.

## Dev preview parity
Stage touches governance pipeline script/docs and regenerated audit artifacts only; no frontend template/layout changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
