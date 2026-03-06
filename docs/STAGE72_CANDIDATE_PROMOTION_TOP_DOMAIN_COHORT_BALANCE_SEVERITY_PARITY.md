# Stage 72 — Candidate Promotion Top-Domain Cohort-Balance Severity Parity

## What changed
- Extended `scripts/pipeline/source_candidate_audit.py` top-domain summary payload with explicit candidate-add cohort fields:
  - `promotion_opportunity_top_domain_candidate_add_id_count`
  - `promotion_opportunity_top_domain_candidate_add_share_percent`
- Added top-domain cohort balance label in summary output:
  - `promotion_opportunity_top_domain_cohort_mix_level` (`candidate_add_heavy` / `balanced` / `candidate_reject_heavy`)
- Enriched per-domain `promotion_opportunity_top_domains` rows with:
  - `candidate_add_share_percent`
  - `candidate_reject_share_percent`
  - `cohort_mix_level`
- Updated markdown report rendering to show top-domain add/reject share, cohort-mix label, and per-domain cohort-mix detail.
- Updated `docs/WEEKLY_PIPELINE.md` to document the added top-domain cohort-balance fields.

## Verification
- Regenerated source-audit artifacts:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

- Confirmed outputs include new cohort-balance fields:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Dev preview parity
Stage changes governance pipeline script/docs and regenerated audit artifacts only; no homepage/template changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
