# Stage 32 — Workflow Dispatch Input Parity

## Objective
Expose `run_weekly.py` execution-mode flags as first-class GitHub Actions `workflow_dispatch` inputs so manual runs can reproduce local/CI-safe behaviors without editing workflow YAML.

## Changes delivered

### 1) Added manual dispatch inputs to workflow
Updated `.github/workflows/weekly-editorial.yml` with optional `workflow_dispatch` inputs:
- `issue_id` (string)
- `skip_buttondown` (boolean)
- `skip_source_audit` (boolean)
- `no_enforce_artifacts` (boolean)

### 2) Added argument builder step
Inserted a new step (`Build pipeline args`) that:
- Reads dispatch inputs from `github.event.inputs`
- Builds a safe argument list
- Emits `pipeline_args` for the run step

### 3) Wired args into pipeline execution
Updated run step to invoke:

```bash
python3 scripts/pipeline/run_weekly.py ${{ steps.pipeline_args.outputs.pipeline_args }}
```

This keeps scheduled behavior unchanged while enabling manual parity with local command flags.

### 4) Documented operator parity
Updated `docs/WEEKLY_PIPELINE.md` to list dispatch input -> CLI flag mapping for clear runbook guidance.

## Verification
- Workflow YAML parses and retains existing Monday 08:00 London schedule gate.
- Manual dispatch now supports issue backfills and safe-run toggles without workflow edits.
- Documentation reflects exact input/flag mapping.

## Local parity reference

```bash
python3 scripts/pipeline/run_weekly.py \
  --issue-id 2026-10 \
  --skip-buttondown \
  --skip-source-audit \
  --no-enforce-artifacts
```
