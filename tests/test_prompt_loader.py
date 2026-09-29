import hashlib
import os
import sys

sys.path.insert(0, ".")
from prompt_app import load_prompt  # noqa: E402


def test_pinned_prompt_file_exists():
    text = load_prompt(os.environ.get("PROMPT_VERSION", "1.2.0"))
    assert "diagnose" in text.lower()


def test_prompt_hash_is_stable():
    text = load_prompt("1.2.0")
    a = hashlib.sha256(text.encode()).hexdigest()
    b = hashlib.sha256(text.encode()).hexdigest()
    assert a == b and len(a) == 64


def test_pin_matches_prompt():
    import json
    from pathlib import Path

    pin = json.loads(Path("prompts/pin.json").read_text(encoding="utf-8"))
    text = load_prompt("1.2.0")
    assert pin["prompt_sha256"] == hashlib.sha256(text.encode()).hexdigest()
