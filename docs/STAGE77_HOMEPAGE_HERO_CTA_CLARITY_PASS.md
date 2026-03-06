# Stage 77 — Homepage Hero CTA Clarity Pass

## What changed
- Added a primary hero CTA button: `Read latest edition` linking to `posts/issue-2026-10.html`.
- Added a secondary hero CTA button: `Browse archive` linking to `archive.html`.
- Preserved the Stage 76 visitor-first hero copy and existing card grid layout.

## Why
The hero message is now clear, but first-time visitors still had to scan the nav/cards before taking action. Explicit CTAs reduce friction and make the intended first click obvious without redesigning the homepage structure.

## Files changed
- `index.html`
- `docs/EXECUTION_QUEUE.md`
- `docs/STAGE77_HOMEPAGE_HERO_CTA_CLARITY_PASS.md`

## Verification
- Homepage render sanity check: hero now shows both CTA buttons with expected targets.
- Link targets verified:
  - `posts/issue-2026-10.html`
  - `archive.html`
- No pipeline/governance scripts changed in this stage.

## Dev preview parity
Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
