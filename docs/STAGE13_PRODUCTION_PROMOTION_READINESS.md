# Stage 13 — Production Promotion Readiness

_Date: 2026-03-02 (UTC)_

## Scope executed

- Re-ran queue validation for latest generated issue dataset (`2026-09`).
- Re-ran internal link integrity checks across root + issue HTML pages.
- Re-validated RSS parseability and issue coverage alignment (`archive.html` vs `feed.xml` vs `posts/issue-*.html`).
- Prepared final promotion checklist and rollback notes for `develop -> main`.

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
# parse feed.xml as RSS and compare coverage with archive + posts
PY
# RSS items: 8
# Archive coverage missing (published html issues): none
# Feed slug coverage missing (published html issues): none
```

## Promote-ready checklist (`develop -> main`)

1. Confirm `develop` includes Stage 9-13 docs and QA evidence (done).
2. Open PR: `develop` -> `main` with links to Stage 9-13 milestone docs.
3. Verify PR diff is content/docs-only (no unintended config/runtime drift).
4. Merge PR and confirm GitHub Pages production build succeeds.
5. Smoke-check production URLs:
   - `/`
   - `/archive.html`
   - `/posts/issue-008.html`
   - `/feed.xml`
6. Post release note with rollback commit reference.

## Rollback notes

- **Fast rollback strategy:** revert production to pre-promotion `main` commit via GitHub revert or hard reset + force push (maintainer-only path).
- **Preferred approach:** PR-based revert of the promotion merge commit to preserve audit trail.
- **Validation after rollback:** rerun URL smoke checks + RSS parse check to confirm restored state.

## Result

Stage 13 completed with no hard blockers. Repository is promotion-ready with final QA evidence and rollback plan documented.
