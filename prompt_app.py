"""AfyaPlus triage API — versioned prompt reported on /health."""
import hashlib
import os
from pathlib import Path

import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field

PROMPTS_DIR = Path("prompts")
CONFIG_PATH = Path("config/triage.yaml")
PROMPT_VERSION = os.environ.get("PROMPT_VERSION", "1.2.0")


def load_config() -> dict:
    if CONFIG_PATH.is_file():
        return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    return {}


def load_prompt(version: str) -> str:
    path = PROMPTS_DIR / f"triage_system_v{version}.txt"
    if not path.is_file():
        raise FileNotFoundError(f"No prompt for version {version!r}: {path}")
    return path.read_text(encoding="utf-8")


CONFIG = load_config()
SYSTEM_PROMPT = load_prompt(PROMPT_VERSION)
PROMPT_SHA256 = hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest()

app = FastAPI(title="AfyaPlus Triage", version="1.2.0")


class TriageIn(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "afyaplus-triage",
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": PROMPT_SHA256,
        "model": CONFIG.get("model", os.environ.get("LLM_MODEL", "gpt-4o-mini")),
        "model_version": CONFIG.get("model_version", "2026.09-stub"),
        "mcp_server_version": CONFIG.get("mcp_server_version", "1.1.0"),
        "image_tag": CONFIG.get("image_tag", "afyaplus-triage:1.2.0"),
    }


@app.post("/triage")
def triage(body: TriageIn):
    return {
        "advice": "(stub — production sends SYSTEM_PROMPT to Week 6 OpenAI client)",
        "prompt_version": PROMPT_VERSION,
        "disclaimer": "Not a diagnosis. Seek professional care when unsure.",
    }


if __name__ == "__main__":
    print("PROMPT_VERSION", PROMPT_VERSION)
    print("PROMPT_SHA256", PROMPT_SHA256)
