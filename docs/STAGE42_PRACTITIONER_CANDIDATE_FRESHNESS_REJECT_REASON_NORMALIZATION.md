# Stage 42 — Practitioner Candidate Freshness + Reject Reason Normalization

## Outcome
- Refreshed discovery candidate metadata to capture current practitioner additions without changing core approved `sources[]`.
- Added two new practitioner candidate feeds for review:
  - `pwmather` (Paul Mather)
  - `allandecastro` (Allan De Castro)
- Normalized reject reasons for feeds that are now endpoint-healthy (`d365goddess`, `powertricks`) from transport-failure wording to editorial-fit/approval wording.
- Re-ran candidate feed audit artifacts for up-to-date evidence.

## Files changed
- `data/sources.json`
- `docs/SOURCE_SHORTLIST.md`
- `artifacts/source_candidate_audit.json`
- `artifacts/source_candidate_audit.md`
- `docs/EXECUTION_QUEUE.md`
- `docs/STAGE42_PRACTITIONER_CANDIDATE_FRESHNESS_REJECT_REASON_NORMALIZATION.md`

## Verification
Executed:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Result:
- Exit code `0`
- Artifacts regenerated:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Notes
- Approval-first guardrail maintained: no promotions into `sources[]` core tracking set.
- `the-custom-engine-github` remains manual-watch/non-ingestable (HTML search URL, not RSS/Atom feed).
