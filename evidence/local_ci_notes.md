# Local CI evidence (Sammy)

All gates reproduced locally on Windows (2026-09-29).

| Step | Log | Result |
|------|-----|--------|
| Ruff | `ruff.log` | All checks passed |
| Pytest | `pytest.log` | 3 passed |
| Eval pass (≥ 0.85) | `eval_pass.log` | `eval_score=1.00` (5/5) |
| Eval fail closed | `eval_fail.log` | Earlier run at threshold 1.0 with 3/5 (exit 1) |
| MCP health pass | `mcp_health_pass.log` | tools + version 1.1.0 |
| MCP health fail demo | `mcp_health_fail.log` | Wrong version prefix → exit 1 |
| Docker build | `deploy_stub.log` | `afyaplus-triage:1.2.0` built OK |
| Image digest | `image_digest.txt` | `sha256:07b404b699c12f63456c52d46824490c0f65a3598a4394bc8c5863f87b96ccfd` |

## GitHub Actions

- Green CI (all jobs): https://github.com/Sammy-CK/WEEK-8-CAPSTONE-PROJECT-CI-CD-PIPELINE-FOR-VERSIONED-AI-PLUS-MCP-HEALTH/actions/runs/36716941727
- Failed CI before MCP pin fix: https://github.com/Sammy-CK/WEEK-8-CAPSTONE-PROJECT-CI-CD-PIPELINE-FOR-VERSIONED-AI-PLUS-MCP-HEALTH/actions/runs/36578912083

Tag **`v1.2.0`** on commit `a84caba` after README update.
