# Stage 78 — Homepage Freshness Signal + Nav CTA Wording Parity

## What changed
- Added a compact freshness line in the homepage hero:
  - `Latest: Week of 2 Mar 2026 · Monday, 02 March 2026 · 11 editions published`
- Updated top-nav CTA wording from `Latest` to `Latest edition` for consistent first-click language.
- Left layout/card structure and pipeline/governance scripts unchanged.

## Why
Stage 77 clarified hero actions, but first-time visitors still had to infer whether the newsletter is current. The new freshness line makes recency explicit without adding visual noise, and nav wording now matches hero CTA phrasing.

## Files changed
- `index.html`
- `docs/EXECUTION_QUEUE.md`
- `docs/STAGE78_HOMEPAGE_FRESHNESS_SIGNAL_NAV_CTA_WORDING_PARITY.md`

## Verification
- Homepage render sanity check confirms freshness line appears under hero intro copy.
- Nav text check confirms `Latest edition` label is present and still targets `posts/issue-2026-10.html`.
- No script or workflow files changed in this stage.

## Dev preview parity
Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.
