# Stage 8 — Final Polish + Production Promotion Plan

_Date: 2026-03-01 (UTC)_

## Scope executed

- Re-ran current-issue queue validation for `2026-09`.
- Re-ran internal link integrity across root + post HTML pages.
- Re-ran RSS parsing and published-issue slug coverage checks.
- Ran a lightweight readability sanity check (word-count floor) across homepage, archive, and issue pages.
- Prepared production promotion checklist for merge to `main`.

## Verification outputs

```bash
python3 scripts/pipeline/validate_queue.py --issue-id 2026-09
# Validation OK: 24 items
```

```bash
python3 - <<'PY'
# regex-based internal href/src existence check
PY
# OK: internal href/src check passed across 13 html files
```

```bash
python3 - <<'PY'
# feed.xml parse
PY
# OK: feed.xml parsed
```

```bash
python3 - <<'PY'
# archive/feed coverage for published html issues issue-001..008
PY
# Archive coverage missing (published html issues): none
# Feed slug coverage missing (published html issues): none
```

```bash
python3 - <<'PY'
# readability word-count check (<120 words flagged)
PY
# Readability word-count check (<120 words flagged): none flagged
```

## Production promotion checklist (develop -> main)

1. Confirm `develop` is green and synced to dev preview (done in this milestone).
2. Open PR: `develop` -> `main` with Stage 8 QA evidence link.
3. Verify PR diff only contains intended content/docs changes.
4. After merge, sync production Pages branch (or let Pages build from `main` automatically).
5. Smoke-check production URLs:
   - `/`
   - `/archive.html`
   - latest published issue page
   - `/feed.xml`
6. Post launch note + rollback pointer (last known-good commit on `main`).

## Result

Stage 8 completed with no hard blockers. Project is promotion-ready from a QA/readability standpoint.
