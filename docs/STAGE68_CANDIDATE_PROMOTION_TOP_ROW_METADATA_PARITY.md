# Stage 68 — Candidate Promotion Top-Row Metadata Parity

## Goal
Make promotion triage faster by exposing human-readable metadata (name/url/reason) on ranked promotion queue rows, so operators can decide from one summary block without opening raw feed tables.

## Changes shipped
- Extended `scripts/pipeline/source_candidate_audit.py` promotion queue rows to include:
  - `name`
  - `url`
  - `ingestability_reason`
- Added `promotion_opportunity_top_rows` (top 5 ranked row objects) to the JSON summary payload for compact, machine-readable triage shortcuts.
- Updated markdown summary queue detail output to include source name + URL and ingestability reason per ranked promotion row.
- Updated `docs/WEEKLY_PIPELINE.md` to document the new `promotion_opportunity_top_rows` summary field.
- Regenerated source-audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification
```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Command completed successfully and rewrote both source-audit artifacts with enriched promotion-row metadata.

## Dev preview parity
Stage changes pipeline governance script/docs and regenerated artifacts only; no homepage/template changes. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
