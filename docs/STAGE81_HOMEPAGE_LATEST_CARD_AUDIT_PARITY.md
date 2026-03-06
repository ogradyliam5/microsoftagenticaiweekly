# Stage 81 — Homepage Latest-Card Audit Parity

## Objective
Close a remaining drift path: homepage `latest edition` text links were audited, but the featured archive card marker (`Start here · Latest edition`) could still silently point at an older issue.

## Changes shipped
- Extended `scripts/pipeline/release_audit.py` with homepage latest-card checks:
  - Parse `index.html` for the card marker `Start here · Latest edition`.
  - Require **exactly one** marker instance.
  - Require the card link slug to match RSS first item slug (`feed.xml`).
- Kept existing latest-link checks intact.
- Updated runbook in `docs/WEEKLY_PIPELINE.md` with the new parity behavior.

## Verification
```bash
python3 scripts/pipeline/release_audit.py --root .
```

Expected result:
- `Index latest-edition link errors: none`
- `Index latest-edition card errors: none`
- `Release audit OK`

## Outcome
Homepage first-click “latest edition” pathways (hero/nav links + featured latest card) now fail fast together when drift occurs, reducing stale-link regressions before `develop -> main` promotion.
