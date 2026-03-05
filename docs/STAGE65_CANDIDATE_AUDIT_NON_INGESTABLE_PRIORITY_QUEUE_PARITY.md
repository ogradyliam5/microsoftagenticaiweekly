# Stage 65 — Candidate Audit Non-Ingestable Priority Queue Parity

## Goal
Add deterministic urgency-ordered non-ingestable queues so source triage can start with the most actionable failures first, without manually scanning reason buckets.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` summary output with:
  - `candidate_add_non_ingestable_priority_ids`
  - `candidate_reject_non_ingestable_priority_ids`
- Added deterministic priority ordering for non-ingestable queues using urgency rank:
  1. `fetch_failed`
  2. `no_items`
  3. `unsupported_root_tag`
  4. `unknown`
- Updated markdown report rendering to print both priority queues in the actionable triage section.
- Updated `docs/WEEKLY_PIPELINE.md` with the new priority queue fields and ranking behavior.
- Regenerated source audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification
```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Command completed successfully and rewrote both audit artifacts with priority queue metadata.

## Dev preview parity
Stage touches governance pipeline script/docs and regenerated audit artifacts only; no frontend template/layout changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
