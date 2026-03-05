# Stage 58 — Candidate Audit Machine-Ingestability Classification

## Goal
Improve source-governance triage by distinguishing endpoint reachability from machine-ingestable feed validity in candidate audit outputs.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` feed status payload with:
  - `root_tag`
  - `machine_ingestable` (requires RSS/Atom-compatible root + non-zero items)
- Added summary counters to audit report output:
  - `candidate_add_non_ingestable`
  - `candidate_reject_now_ingestable`
- Updated markdown report lines to surface root tag, item count, and ingestability classification for each candidate/rejected endpoint.
- Updated `docs/WEEKLY_PIPELINE.md` to document ingestability classification behavior.
- Regenerated source audit artifacts with the updated schema:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification evidence
Command:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Observed output:
- `artifacts/source_candidate_audit.json` written with ingestability metadata + counters.
- `artifacts/source_candidate_audit.md` written with per-row root/item/ingestability details.

## Dev preview parity
Stage touches pipeline governance script/docs and regenerated artifacts only; no frontend template/layout changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
