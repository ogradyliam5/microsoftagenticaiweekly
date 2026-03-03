# Stage 27 — Candidate Feed Health Audit Automation

## Objective
Automate feed-health verification for discovery candidates and rejected feeds so source promotion decisions are evidence-based and repeatable.

## Changes delivered
- Added `scripts/pipeline/source_candidate_audit.py`.
  - Reads `data/sources.json` candidate `add` + `reject` lists.
  - Checks HTTP/feed parse status for each URL.
  - Emits both JSON and markdown artifacts.
- Generated fresh audit artifacts:
  - `artifacts/source_candidate_audit.json`
  - `artifacts/source_candidate_audit.md`

## Verification command (local parity)
```bash
python3 scripts/pipeline/source_candidate_audit.py
```

## Current audit snapshot (2026-03-03)
- Candidate add feeds healthy: **4/4**
- Candidate add feeds failing: **0/4**
- Rejected feeds still blocked: **2/7** (`holgerimbery` 404, `tom-riha` 403)
- Rejected feeds now reachable: **5/7** (flagged for manual policy/quality review, not auto-promotion)

## Guardrails preserved
- No core `sources[]` promotions were performed.
- Approval-first policy remains unchanged; this stage adds only audit tooling + evidence.

## Evidence
- `scripts/pipeline/source_candidate_audit.py`
- `artifacts/source_candidate_audit.json`
- `artifacts/source_candidate_audit.md`
- `docs/EXECUTION_QUEUE.md`
