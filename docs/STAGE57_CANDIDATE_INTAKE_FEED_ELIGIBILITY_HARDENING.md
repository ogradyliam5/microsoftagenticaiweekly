# Stage 57 — Candidate Intake Feed Eligibility Hardening

## Goal
Keep discovery candidates machine-ingestable by removing manual-watch/non-feed endpoints from `candidates.add`, while refreshing practitioner candidates and audit evidence.

## Changes shipped
- Refreshed discovery metadata timestamps in `data/sources.json` (`updated_at` and `candidates.updated_at`).
- Added two parseable practitioner RSS candidates:
  - `itaintboring` (`https://www.itaintboring.com/feed/`)
  - `benitezhere` (`https://benitezhere.blogspot.com/feeds/posts/default?alt=rss`)
- Removed non-ingestable manual-watch item `the-custom-engine-github` from `candidates.add`.
- Added `the-custom-engine-github` into `candidates.reject` with normalized reason (not a machine-ingestable RSS/Atom feed).
- Updated `docs/SOURCE_SHORTLIST.md` to reflect candidate intake policy and revised shortlist.
- Re-ran source candidate audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification evidence
Command:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Key output (`artifacts/source_candidate_audit.md`):
- Candidate add feeds healthy: **8**
- Candidate add feeds failing: **0**
- New candidates `itaintboring` and `benitezhere` both returned HTTP 200 and parseable feed items.
- `the-custom-engine-github` remains non-feed/non-ingestable and is now normalized under reject inventory.

## Dev preview parity
Stage modifies source governance data and docs only; no frontend rendering regressions observed. Dev preview sync executed via `./scripts/sync-dev-site.sh` after commit.