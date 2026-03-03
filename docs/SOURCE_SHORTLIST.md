# Source Shortlist (Stage 1 Stabilization)

_Last updated: 2026-03-03 06:30 UTC_

Promotions remain unchanged in this run. This pass focused on fresh practitioner discovery and candidate hygiene (dedupe + feed validation).

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

## Discovery candidates pending approval

- `lowcodelewis` — Low Code Lewis (`https://lowcodelewis.com/feed/`)
  - Why: strong Copilot Studio + Dataverse practitioner posts; recent agent-focused content; parseable active RSS.
- `platformsofpower` — Platforms of Power (Craig White) (`https://platformsofpower.net/feed/`)
  - Why: governance/ops depth (DLP, connector policy, Entra identities for Copilot Studio); high fit for weekly audience.
- `joegill` — Joe Gill (`https://joegill.com/feed/`)
  - Why: practical Dataverse/ALM implementation notes; consistent technical signal over marketing.
- `benedikt-bergmann` — Benedikt Bergmann (`https://benediktbergmann.eu/feed/`)
  - Why: strong ALM/operations content; lower AI density but still relevant to governance/ops lane.

## Rejected / excluded (keep out of automated ingestion)

- `holgerimbery` — 404 feed endpoint
- `powertricks` — 406 feed endpoint
- `mmsharepoint` — stale cadence for current weekly format
- `medium-tag-powerplatform` — high-noise tag aggregator
- `medium-tag-microsoft365` — high-noise tag aggregator
- `tom-riha` — 403 feed endpoint (blocked for automated retrieval)
- `d365goddess` — 406 feed endpoint

## Validation notes

- Dedupe check completed against existing `sources[]` ids + URLs before updating candidates.
- No core `sources[]` changes made (approval-first policy preserved).
- Candidate additions are discovery-only and await Liam approval before promotion.
- `azure-updates` remains in core official list with known XML parsing fragility; continue monitoring.
