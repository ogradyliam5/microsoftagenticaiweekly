# Source Shortlist (Stage 1 Stabilization)

_Last updated: 2026-03-01 17:20 UTC_

Promotions have now been applied to core `sources[]` in `data/sources.json` for validated practitioner feeds. Broken/unreliable feeds remain excluded.

## Promoted to core sources (approved set)

- `futurework-blog` — Future Work (Vesa Nopanen)
- `reshmee-auckloo` — Reshmee Auckloo
- `baeke` — Geert Baeke
- `rob-quickenden` — Rob Quickenden
- `karlex` — Karl-Johan Spiik (Karlex)
- Prior approved practitioner additions retained in core:
  - `forwardforever`
  - `megan-v-walker`
  - `nishant-rana`
  - `readyxrm`
  - `eliostruyf`
  - `sharepains`
  - `michelcarlo`

## Discovery candidates still pending

- None at this time.

## Rejected / excluded (keep out of automated ingestion)

- `holgerimbery` — 404 feed endpoint
- `powertricks` — 406 feed endpoint
- `mmsharepoint` — stale cadence for current weekly format
- `medium-tag-powerplatform` — high-noise tag aggregator
- `medium-tag-microsoft365` — high-noise tag aggregator

## Validation notes

- Promoted feeds were validated as parseable RSS/Atom sources.
- Rejected endpoints remain excluded from core sources.
- `azure-updates` stays in core official list but has known XML parsing fragility and should be monitored.
