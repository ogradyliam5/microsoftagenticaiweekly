# Execution Queue (PM-controlled)

Purpose: prevent stop/start drift and force delivery through ordered stages.

## Rules
- Work in strict stage order.
- No stage is considered complete without:
  1) commit hash,
  2) file list,
  3) dev preview sync confirmation.
- Progress updates must include tangible outputs only.
- If interrupted by chat/system events, resume current stage immediately.
- Never idle between stages: immediately dispatch next stage/subagent unless a hard blocker exists.
- Overnight mode: continue autonomous execution without waiting for user pings; send milestone updates with proof only.
- PM cadence: checkpoint updates are outcome-based (not time-based) and must include next concrete step already in progress.

## Stage Plan

### Stage 1 — Source Engine Stabilization
- Promote approved practitioner candidates into tracked sources.
- Validate feed health and mark hard failures.
- Regenerate queue + draft artifacts.

### Stage 2 — Content Quality Pass
- Improve issue copy quality for Jan/Feb issues (#001-#008):
  - clearer "why it matters"
  - role-targeting (Builder/Platform Owner/Leader)
  - action signal labels.

### Stage 3 — Frontend Redesign Iteration 2
- Replace homepage and archive framing with cleaner cross-stack messaging.
- Keep provenance and approval-first cues.

### Stage 4 — Final QA + Release Readiness
- Link checks, metadata consistency, feed correctness, schedule notes.
- Publish final dev sync and handoff checklist.

## Stage completion log

- [x] Stage 1 complete — `ee0d109`
- [x] Stage 2 complete — `a4b2627`
- [x] Stage 3 complete — `e2c7c5f`
- [x] Stage 4 complete — see `docs/STAGE4_QA_RELEASE_READINESS.md` (this run)
