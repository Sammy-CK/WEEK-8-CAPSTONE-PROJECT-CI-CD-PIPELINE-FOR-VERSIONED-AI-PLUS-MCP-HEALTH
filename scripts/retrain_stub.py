"""Stub retrain job — no GPU; bumps model_version in config and CHANGELOG."""
from pathlib import Path

CONFIG = Path("config/triage.yaml")
CHANGELOG = Path("CHANGELOG.md")


def main() -> None:
    lines = CONFIG.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if line.startswith("model_version:"):
            out.append('model_version: "2026.09-retrain-stub"')
        else:
            out.append(line)
    CONFIG.write_text("\n".join(out) + "\n", encoding="utf-8")
    note = (
        "\n## [2026.09-stub-retrain] - stub CI job\n"
        "- No weights trained; model_version bumped only.\n"
    )
    CHANGELOG.write_text(CHANGELOG.read_text(encoding="utf-8") + note, encoding="utf-8")
    print("retrain stub complete — model_version bumped, CHANGELOG updated")


if __name__ == "__main__":
    main()
