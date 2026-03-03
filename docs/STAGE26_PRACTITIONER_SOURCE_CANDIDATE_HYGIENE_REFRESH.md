# Stage 26 — Practitioner Source Candidate Hygiene Refresh

## Objective
Refresh discovery-only practitioner source candidates so weekly ingestion can promote higher-signal creators without changing approved core tracked sources.

## Changes delivered
- Updated `data/sources.json` timestamps to reflect the latest candidate review window.
- Added four new **candidate-only** practitioner RSS feeds:
  - `lowcodelewis`
  - `platformsofpower`
  - `joegill`
  - `benedikt-bergmann`
- Added/reinforced reject records for feeds that are operationally unsuitable:
  - `d365goddess` (HTTP 406)
  - `tom-riha` (HTTP 403)
  - Medium tag feeds retained as high-noise rejects
  - `powertricks` retained as HTTP 406 reject
- Updated `docs/SOURCE_SHORTLIST.md` with approval-ready rationale, explicit “no core source promotions” statement, and validation notes.

## Guardrails preserved
- No changes were made to approved core `sources[]` entries.
- Discovery remains approval-first: candidates are queued for Liam review before promotion.
- Reject reasons are explicit to reduce repeated failed ingestion checks.

## Evidence
- `data/sources.json`
- `docs/SOURCE_SHORTLIST.md`
- `docs/EXECUTION_QUEUE.md`
