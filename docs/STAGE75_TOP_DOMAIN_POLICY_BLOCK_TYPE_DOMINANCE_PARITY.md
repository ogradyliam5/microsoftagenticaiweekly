# Stage 75 — Top-Domain Policy Block-Type Dominance Parity

## What changed
- Extended `scripts/pipeline/source_candidate_audit.py` summary output to add top-domain policy-blocked type breakdown + dominance metadata:
  - `promotion_opportunity_top_domain_policy_blocked_counts_by_type`
  - `promotion_opportunity_top_domain_policy_blocked_percentages_by_type`
  - `promotion_opportunity_top_domain_policy_blocked_top_type`
  - `promotion_opportunity_top_domain_policy_blocked_top_type_share_percent`
  - `promotion_opportunity_top_domain_policy_blocked_top_type_ids`
- Reused existing policy block-type priority ordering to keep deterministic dominant-type selection.
- Updated markdown audit rendering so top-domain policy-blocked lines include per-type percentages and a one-line dominant top-domain block-type summary.
- Updated `docs/WEEKLY_PIPELINE.md` with the new top-domain policy block-type summary fields.

## Verification
- Regenerated source-candidate audit artifacts:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

- Confirmed new top-domain dominance/breakdown fields in:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Dev preview parity
Stage changes governance pipeline script/docs and regenerated audit artifacts only; no homepage/template changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
