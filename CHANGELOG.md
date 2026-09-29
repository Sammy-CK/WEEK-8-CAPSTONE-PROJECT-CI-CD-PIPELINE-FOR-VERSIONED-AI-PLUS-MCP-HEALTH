# Changelog — AfyaPlus versioned triage + MCP

Format: Keep a Changelog. Versioning: SemVer.

## [1.2.0] - 2026-09-29

### Added
- CI pipeline: lint-test → eval → mcp-health → deploy stub
- Golden-set eval gate (threshold 0.85) on fixture responses
- MCP server **1.1.0** with `list_low_stock` (additive)

### Prompts
- Production pin: `triage_system_v1.2.0.txt` (SHA in `prompts/pin.json`)
- Candidate: `triage_system_v1.3.0-candidate.txt` for 10% A/B staging

## [1.1.0] - MCP logistics

### Added
- `list_low_stock(clinic_id)`
- Resource `version://current` reports **1.1.0**

## [1.0.0] - Week 6 baseline

- JWT triage API and logistics MCP tools (see Week 6 capstone)
