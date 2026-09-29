import hashlib
import os
from pathlib import Path

PROMPTS = Path("prompts")


def load_prompt(version: str) -> str:
    return (PROMPTS / f"triage_system_v{version}.txt").read_text(encoding="utf-8")


def assign_variant(user_key: str, pct_b: int = 10) -> str:
    bucket = int(hashlib.sha256(user_key.encode()).hexdigest(), 16) % 100
    return "B" if bucket < pct_b else "A"


def select_prompt(user_key: str) -> tuple[str, str, str]:
    pct = int(os.getenv("PROMPT_B_PCT", "10"))
    variant = assign_variant(user_key, pct)
    version = os.getenv(
        f"PROMPT_{variant}_VERSION",
        "1.2.0" if variant == "A" else "1.3.0-candidate",
    )
    return variant, version, load_prompt(version)
