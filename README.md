# Week 8 Capstone — CI/CD for Versioned AI + MCP Health

**AfyaPlus** triage prompt, config, and logistics MCP are versioned together. GitHub Actions runs lint → golden-set eval (fails closed at **0.85**) → MCP stdio health → Docker deploy stub on `main`. Azure Pipelines mirrors the same stages for org templates.

## Release alignment (v1.2.0)

| Item | Value |
|------|--------|
| Git tag | `v1.2.0` |
| Docker | `afyaplus-triage:1.2.0` |
| Prompt | `1.2.0` — SHA in `prompts/pin.json` |
| MCP | `1.1.0` |

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env   # optional; eval uses fixtures, not OpenAI

pytest -q
python eval_prompts.py --threshold 0.85
python scripts/check_mcp_health.py
uvicorn prompt_app:app --port 8000
```

## Repository layout

- `prompts/` — versioned system prompts + `pin.json`
- `config/triage.yaml` — model and MCP version pins
- `evals/golden.jsonl` — golden cases (urgency + safety strings)
- `fixtures/responses/<prompt_sha256>.json` — deterministic eval responses
- `logistics_mcp_versioned.py` — MCP server (stdio)
- `scripts/check_mcp_health.py` — CI MCP gate
- `.github/workflows/ci.yml` — primary pipeline
- `azure-pipelines.yml` — Azure DevOps equivalent
- `runbook.md` — roll forward / back, DoD
- `clinical_ops_change_brief.md` — clinical go/no-go
- `evidence/` — local CI reproduction logs

## CI gates

1. **lint-test** — Ruff + pytest  
2. **eval** — `eval_prompts.py`; exit 1 if score < threshold  
3. **mcp-health** — lists tools, checks `version://current` prefix **1.1.0**  
4. **deploy-stub** — `docker build -t afyaplus-triage:1.2.0 .` on push to `main`

Manual **workflow_dispatch** runs the optional **retrain-stub** job (bumps `model_version` only).

## Governance

- `prompts/` and `evals/` require review via `.github/CODEOWNERS` (clinical_ops / ml-eng placeholders).
- Engineering **recommends** release readiness; **clinical_ops decides** on patient-facing wording (`clinical_ops_change_brief.md`).

## Weeks 6–7 lineage

Built on Week 6 JWT triage + MCP patterns and Week 7 cost-aware ops (fixture eval avoids API spend in CI).

## Author

Sammy — Week 8 LLMOps capstone submission.
