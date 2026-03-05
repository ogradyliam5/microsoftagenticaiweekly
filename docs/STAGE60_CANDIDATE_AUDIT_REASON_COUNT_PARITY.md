# Stage 60 — Candidate Audit Reason-Count Parity

## Objective
Add explicit ingestability-reason count breakdowns for both candidate-add and candidate-reject cohorts so source triage can quickly identify endpoint failures vs machine-ingestable promotion opportunities.

## Changes shipped
- Updated `scripts/pipeline/source_candidate_audit.py`:
  - Added standardized reason set (`machine_ingestable`, `no_items`, `unsupported_root_tag`, `fetch_failed`, `unknown`).
  - Added summary maps:
    - `summary.candidate_add_reason_counts`
    - `summary.candidate_reject_reason_counts`
  - Added markdown report section: **Ingestability reason breakdown** for both cohorts.
- Regenerated source audit artifacts with refreshed counters:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`
- Updated runbook documentation:
  - `docs/WEEKLY_PIPELINE.md`

## Verification
Local parity command:

```bash
python3 scripts/pipeline/source_candidate_audit.py
```

Observed summary evidence in `artifacts/source_candidate_audit.json`:
- `candidate_add_reason_counts.fetch_failed = 4`
- `candidate_reject_reason_counts.fetch_failed = 3`
- `candidate_reject_reason_counts.machine_ingestable = 5`

## Outcome
Candidate/reject source triage now has cohort-level reason counts that make approval/rejection discussions faster and more evidence-driven without changing approval-first source policy.
