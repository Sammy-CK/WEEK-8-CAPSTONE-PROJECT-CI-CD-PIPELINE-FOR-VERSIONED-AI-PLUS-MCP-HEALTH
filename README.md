# Week 8 — CI/CD for Versioned AI + MCP Health

## Overview

AfyaPlus triage **prompts**, **config**, and **logistics MCP** are versioned with semver and a pinned SHA. GitHub Actions gates every change: **lint-test → eval (fixture golden set) → MCP stdio health → deploy stub** (`docker build`). A failing eval or MCP probe **fails closed**; deploy does not run. Azure DevOps YAML mirrors the same stages. Retrain is optional: `scripts/retrain_stub.py` only bumps `model_version` and updates `CHANGELOG.md` (no GPU).

## Versions

| Artefact | Value |
|----------|--------|
| Git tag (release) | `v1.2.0` |
| Image tag | `afyaplus-triage:1.2.0` |
| Prompt (production) | `1.2.0` — candidate `1.3.0-candidate` for A/B |
| Prompt SHA | `prompts/pin.json` → `079e4fe811f836ce288ae4b227e45466b77d6c98b9ad3476f2b3342c6d1b0331` |
| Config / model_version | `config/triage.yaml` — `2026.09-stub` |
| MCP server | `1.1.0` (`version://current`) |

Runtime evidence: `GET /health` on `prompt_app.py` (also `evidence/docker_health.log`).

## Pipeline

- **Workflow:** `.github/workflows/ci.yml` (on `pull_request`, `push` to `main`, `workflow_dispatch`)
- **Twin:** `azure-pipelines.yml`
- **Green CI run (all jobs, incl. deploy-stub):** https://github.com/Sammy-CK/WEEK-8-CAPSTONE-PROJECT-CI-CD-PIPELINE-FOR-VERSIONED-AI-PLUS-MCP-HEALTH/actions/runs/36718170311
- **Failed run (MCP 2.x, fixed by pin):** https://github.com/Sammy-CK/WEEK-8-CAPSTONE-PROJECT-CI-CD-PIPELINE-FOR-VERSIONED-AI-PLUS-MCP-HEALTH/actions/runs/36578912083

| Stage | Job | Command |
|-------|-----|---------|
| lint | `lint-test` | `ruff check .`, `pytest -q` |
| eval | `eval` | `python eval_prompts.py --threshold 0.85` |
| MCP | `mcp-health` | `python scripts/check_mcp_health.py` |
| deploy | `deploy-stub` | `docker build -t afyaplus-triage:1.2.0 .` *(push to `main` only)* |

Local mirror logs: `evidence/` (ruff, pytest, eval pass/fail, MCP pass/fail, docker build).

## Eval gate

- **Metric:** golden-case pass rate on label + `must_include` / `must_not` (fixture responses, no paid API).
- **Threshold:** **0.85** (documented in `eval_prompts.py` and CI).
- **Fixtures:** `evals/golden.jsonl`, `fixtures/responses/<prompt_sha256>.json`
- **Failing run:** `evidence/eval_fail.log` — score **0.60** at threshold **1.0**, exit code **1** (gate blocks). After fixture alignment, pass run is `evidence/eval_pass.log` (**1.00**).

## MCP health

```bash
python scripts/check_mcp_health.py
```

Asserts tools include `check_stock` and `list_low_stock`, and `version://current` starts with `1.`. Non-zero exit fails the CI job before `deploy-stub`. Fail demo: `evidence/mcp_health_fail.log`.

## Runbook and Definition of Done

- **Runbook:** [runbook.md](runbook.md) — roll forward/back, traces, version table.
- **Clinical brief:** [clinical_ops_change_brief.md](clinical_ops_change_brief.md) — go/no-go for clinical_ops.
- **Sprint DoD:** checklist in `runbook.md` (pin, golden fixtures, eval, MCP, brief, CODEOWNERS).
- **Governance:** engineering **recommends** readiness from CI; **clinical_ops decides** on patient-facing prompt promotion (see brief + runbook).

## Fallbacks declared

- [x] Local CI logs + `workflow_dispatch` (no `act` required; same YAML as cloud)
- [x] Stub retrain (`scripts/retrain_stub.py` — `model_version` bump only)
- [x] Local MCP stdio stub (`logistics_mcp_versioned.py`) — same exit-code contract as CI
- [x] No paid OpenAI in CI — fixture eval only (~$0)
- [x] No Azure deploy — `azure-pipelines.yml` as config-as-code; primary path is GitHub Actions
- [x] Deploy ends at **docker build/tag**; digest in `evidence/image_digest.txt` and runbook

## Weeks 6 and 7 reuse

- **Week 6:** FastAPI triage service pattern, MCP tools (`check_stock`), Docker tagging, `clinics.json`.
- **Week 7:** Cost discipline — CI uses stub/fixture paths instead of live LLM calls; health and ops mindset in runbook.

Repo layout matches the capstone brief (`prompts/`, `config/`, `evals/`, `.github/workflows/ci.yml`, `scripts/check_mcp_health.py`, etc.). Extra folder: `evidence/` for local run artefacts.

## Checklist

- [x] Tag alignment evidenced (`prompts/pin.json`, config, image tag, git tag `v1.2.0`)
- [x] Eval fails closed (CI + `evidence/eval_fail.log`)
- [x] MCP health in pipeline (before deploy-stub)
- [x] Runbook, Definition of Done, clinical brief, governance note
- [x] GitHub Actions green run link in Pipeline section
- [x] Git tag `v1.2.0` on `main` (commit `81a6b39`)

## Author

Sammy — Week 8 capstone submission.
