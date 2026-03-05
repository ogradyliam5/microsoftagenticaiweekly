# Source Shortlist (Stage 1 Stabilization)

_Last updated: 2026-03-05 06:30 UTC_

No core `sources[]` promotions in this run (approval-first policy preserved). This pass added two new practitioner candidates and removed one non-ingestable/manual-watch item from candidate intake.

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

- `itaintboring` — It Ain't Boring (Alex Shlega) (`https://www.itaintboring.com/feed/`)
  - Why: independent practitioner with recent Copilot Studio troubleshooting/agent behavior posts plus practical Dataverse depth.
- `benitezhere` — Benitez Here (Gonzalo Ruiz) (`https://benitezhere.blogspot.com/feeds/posts/default?alt=rss`)
  - Why: long-running individual practitioner source with Dataverse + Power Automate implementation guidance relevant to M365 extensibility and governance/ops.
- `lowcodelewis` — Low Code Lewis (`https://lowcodelewis.com/feed/`)
- `platformsofpower` — Platforms of Power (Craig White) (`https://platformsofpower.net/feed/`)
- `joegill` — Joe Gill (`https://joegill.com/feed/`)
- `benedikt-bergmann` — Benedikt Bergmann (`https://benediktbergmann.eu/feed/`)
- `pwmather` — Paul Mather (`https://pwmather.wordpress.com/feed/`)
- `allandecastro` — Allan De Castro (`https://www.blog.allandecastro.com/feed/`)

## Rejected / excluded (keep out of automated ingestion)

- `the-custom-engine-github` — removed from candidates: non-blog/non-feed manual watch link
- `holgerimbery` — 404 feed endpoint
- `tom-riha` — 403 feed endpoint (blocked for automated retrieval)
- `mmsharepoint` — stale cadence for current weekly format
- `medium-tag-powerplatform` — high-noise tag aggregator
- `medium-tag-microsoft365` — high-noise tag aggregator
- `powertricks` — endpoint healthy but excluded pending manual quality/topicality review
- `d365goddess` — endpoint healthy but excluded pending manual quality/topicality review

## Validation notes

- Dedupe check completed against existing `sources[]` ids + URLs before updating candidates.
- No core `sources[]` changes made (approval-first policy preserved).
- Candidate additions are discovery-only and await Liam approval before promotion.
- New additions were validated as reachable RSS feeds and screened for topical fit against Copilot Studio / Dataverse / governance-adjacent content.
