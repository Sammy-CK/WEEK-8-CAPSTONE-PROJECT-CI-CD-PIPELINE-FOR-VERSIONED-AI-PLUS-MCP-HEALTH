# Change-control brief (clinical_ops)

**To:** Clinical operations, AfyaPlus  
**From:** Sammy  
**Date:** September 2026

## What changed

Triage prompt **1.2.0 → 1.3.0-candidate** on **10%** of staging API keys (A/B flag). Production pin stays **1.2.0** until eval and MCP gates pass.

## What was tested

- Golden set: `evals/golden.jsonl` (urgency labels, `must_include`, `must_not`)
- CI prints `eval_score` — must be **≥ 0.85**
- MCP handshake lists `check_stock` and `list_low_stock`; version **1.1.0**

## Rollback

1. Set `PROMPT_VERSION=1.2.0` (same Docker image tag `afyaplus-triage:1.2.0`)
2. Redeploy from git tag **`v1.2.0`**
3. Confirm `/health` shows prompt SHA matching `prompts/pin.json`

## Who approved

- **clinical_ops** and **ml-eng** via CODEOWNERS on the pull request (replace PR # with your number after merge)

## Go / no-go

**Go** if:

- Eval is green (`eval_score ≥ 0.85`)
- MCP handshake lists `check_stock`
- Tool **error_rate** stays under **0.10** (see `tool_metrics.py` / runbook)

**No-go** if eval fails, MCP health fails, or quarantined golden cases spike.

## Governance note (recommend vs decide)

This pipeline **recommends** release readiness; **clinical_ops decides** whether patient-facing wording ships. Engineering does not auto-promote prompt candidates to 100% traffic without clinical sign-off.
