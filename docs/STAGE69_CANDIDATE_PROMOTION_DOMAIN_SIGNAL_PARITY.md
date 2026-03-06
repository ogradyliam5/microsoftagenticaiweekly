# Stage 69 — Candidate Promotion Domain Signal Parity

## Goal
Add domain-level concentration signals to the promotion opportunity queue so source approvals can quickly spot over-concentration and maintain practitioner diversity.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` promotion queue rows with `domain` metadata.
- Added promotion domain summary fields to audit JSON:
  - `promotion_opportunity_domain_counts`
  - `promotion_opportunity_top_domains`
  - `promotion_opportunity_top_domain_ids`
- Updated markdown source-audit output with top-domain summary and domain detail on ranked promotion rows.
- Updated `docs/WEEKLY_PIPELINE.md` to document new promotion-domain signal fields.
- Regenerated source-audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification
```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Command completed successfully and rewrote source-audit artifacts with promotion domain concentration metadata.

## Dev preview parity
Stage changes pipeline governance script/docs and regenerated artifacts only; no homepage/template changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
