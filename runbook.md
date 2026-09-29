# LLMOps runbook — AfyaPlus CI/CD

## Version alignment

| Artefact | Version |
|----------|---------|
| Git tag | `v1.2.0` |
| Docker image | `afyaplus-triage:1.2.0` |
| Prompt (prod) | `1.2.0` — SHA in `prompts/pin.json` |
| MCP server | `1.1.0` — `version://current` |
| Config | `config/triage.yaml` |

Check runtime: `GET /health` on port 8000.

## Pipeline stages (`.github/workflows/ci.yml`)

1. **lint-test** — `ruff check .`, `pytest -q`
2. **eval** — `python eval_prompts.py --threshold 0.85` (fails closed)
3. **mcp-health** — `python scripts/check_mcp_health.py`
4. **deploy-stub** — `docker build -t afyaplus-triage:1.2.0 .` (main only)

## Roll forward

1. Merge PR with prompt/MCP changes
2. Wait for green CI on `main`
3. Tag: `git tag v1.2.0` (or next semver)
4. Deploy image digest recorded in CI artefact / `evidence/deploy_stub.log`

## Roll back

1. Set `PROMPT_VERSION=1.2.0` in environment
2. Redeploy previous image digest or rebuild from tag `v1.2.0`
3. Re-run `eval_prompts.py` locally to confirm green
4. Notify clinical_ops (see `clinical_ops_change_brief.md`)

## Traces and logs

- API: uvicorn stdout; include `prompt_version` from `/health`
- MCP: `mcp_server.log` (one line per tool call)
- CI: GitHub Actions run URL or local logs in `evidence/`

## Sprint Definition of Done (prompt / MCP PRs)

- [ ] Prompt or MCP change has semver / CHANGELOG entry
- [ ] `prompts/pin.json` updated if production prompt SHA changed
- [ ] Golden fixtures updated or quarantined (`fixtures/quarantine.json`)
- [ ] `pytest` and `eval_prompts.py` pass locally
- [ ] `scripts/check_mcp_health.py` exit 0
- [ ] `clinical_ops_change_brief.md` updated for patient-facing wording
- [ ] CODEOWNERS review on `prompts/` and `evals/`

## Weeks 6 and 7 reuse

- **Week 6:** JWT triage + MCP tool patterns; Docker tag discipline (`afyaplus-platform:1.0.0` → this repo uses `afyaplus-triage:1.2.0`)
- **Week 7:** Cost and health mindset — stub eval avoids API spend; budget alerts optional in prod

## Local reproduce

```bash
pip install -r requirements.txt
pytest -q
python eval_prompts.py --golden evals/golden.jsonl --threshold 0.85
python scripts/check_mcp_health.py
docker build -t afyaplus-triage:1.2.0 .
uvicorn prompt_app:app --port 8000
```
