# Source Shortlist (Stage 1 Stabilization)

_Last updated: 2026-03-04 06:30 UTC_

No core `sources[]` promotions in this run (approval-first policy preserved). This pass added two new practitioner candidates and refreshed candidate/reject feed health.

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
  - Why: strong ALM/operations content; lower AI density but relevant to governance/ops lane.
- `pwmather` — Paul Mather (`https://pwmather.wordpress.com/feed/`)
  - Why: active 2026 Copilot Studio hands-on series with end-user + builder walkthroughs; practical implementation detail.
- `allandecastro` — Allan De Castro (`https://www.blog.allandecastro.com/feed/`)
  - Why: practitioner content on Copilot Studio extensions in Dynamics 365 plus Dataverse architecture tooling; implementation-first.
- `the-custom-engine-github` — The Custom Engine (GitHub watch) (`https://github.com/search?q=%22The+Custom+Engine%22&type=repositories`)
  - Why: requested editorial watch lane; still manual-watch only because this URL is not a valid RSS/Atom feed.

## Rejected / excluded (keep out of automated ingestion)

- `holgerimbery` — 404 feed endpoint
- `tom-riha` — 403 feed endpoint (blocked for automated retrieval)
- `mmsharepoint` — stale cadence for current weekly format
- `medium-tag-powerplatform` — high-noise tag aggregator
- `medium-tag-microsoft365` — high-noise tag aggregator
- `powertricks` — endpoint now healthy but remains excluded pending manual quality/topicality review
- `d365goddess` — endpoint now healthy but remains excluded pending manual quality/topicality review

## Validation notes

- Dedupe check completed against existing `sources[]` ids + URLs before updating candidates.
- No core `sources[]` changes made (approval-first policy preserved).
- Candidate additions are discovery-only and await Liam approval before promotion.
- Candidate/reject feed health re-checked via `python3 scripts/pipeline/source_candidate_audit.py` (see `artifacts/source_candidate_audit.md`).
- `the-custom-engine-github` remains non-ingestable as RSS/Atom; keep as manual-watch until a valid feed is found.
- `azure-updates` remains in core official list with known XML parsing fragility; continue monitoring.
