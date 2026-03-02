# Stage 9 — Buttondown Reliability Hardening

_Date: 2026-03-02 (UTC)_

## Scope executed

- Hardened `scripts/pipeline/buttondown_draft.py` for 422/invalid-id recovery without blocking pipeline artifacts.
- Added subject-based idempotent recovery path:
  - If stored draft ID fails (`404`/`422`), script now searches existing drafts by subject and updates matching draft before creating new.
  - If no stored ID exists, script first checks for existing matching-subject draft and updates it (prevents duplicates).
- Added safer fallback for `POST /emails` returning `422`: perform matching-subject lookup + patch recovery before giving up.
- Kept failure mode non-blocking with explicit structured error logs.

## Verification output

```bash
python3 scripts/pipeline/buttondown_draft.py --issue-id 2026-09 --subject "Microsoft Agentic AI Weekly — Issue 2026-09" --body-file drafts/email-2026-09.md
# {"level":"info","message":"Buttondown draft sync complete",...,"action":"created"}
```

```bash
python3 scripts/pipeline/buttondown_draft.py --issue-id 2026-09 --subject "Microsoft Agentic AI Weekly — Issue 2026-09" --body-file drafts/email-2026-09.md
# {"level":"info","message":"Buttondown draft sync complete",...,"action":"updated"}
```

## Result

Stage 9 completed: Buttondown draft sync now has stronger idempotency and recovery behavior around HTTP 422/unusable stored IDs while preserving non-blocking weekly pipeline behavior.
