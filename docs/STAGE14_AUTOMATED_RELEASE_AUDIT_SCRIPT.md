# Stage 14 — Automated Release Audit Script

_Date: 2026-03-02 (UTC)_

## Scope executed

- Added `scripts/pipeline/release_audit.py` to consolidate production-readiness checks in one command.
- Implemented combined validation for:
  1. internal local `href/src` targets,
  2. archive issue coverage,
  3. RSS (`feed.xml`) issue coverage.
- Updated execution queue with Stage 14 plan + completion record.

## Verification output

```bash
python3 scripts/pipeline/release_audit.py --root .
# Audited HTML files: 13
# Published issues: 8
# Archive missing issues: none
# Feed missing issues: none
# Release audit OK
```

## Result

Stage 14 completed with repeatable one-command QA evidence for `develop -> main` promotion checks.
