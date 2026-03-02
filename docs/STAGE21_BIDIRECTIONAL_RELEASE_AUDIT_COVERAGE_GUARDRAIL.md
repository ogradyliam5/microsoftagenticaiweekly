# Stage 21 — Bidirectional Release Audit Coverage Guardrail

_Date: 2026-03-02 (UTC)_

## Scope executed

- Extended `scripts/pipeline/release_audit.py` with two new failure checks:
  1. `archive_stale`: issues referenced in `archive.html` but missing from `posts/`
  2. `feed_stale`: issues referenced in `feed.xml` but missing from `posts/`
- Kept existing checks for internal links + missing archive/feed issue coverage.
- Updated execution queue with Stage 21 plan + completion record.

## Verification output

```bash
python3 scripts/pipeline/release_audit.py --root .
# Audited HTML files: 16
# Published issues: 11
# Archive missing issues: none
# Feed missing issues: none
# Archive stale issues: none
# Feed stale issues: none
# Release audit OK
```

## Result

Stage 21 completed with bidirectional archive/feed coverage checks so release audits now fail on both missing and stale issue references before `develop -> main` promotion.
