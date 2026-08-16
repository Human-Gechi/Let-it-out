import json
import random
from pathlib import Path

from fastapi import APIRouter, Query

from backend.app.schemas import PromptResponse, RecipientType
from backend.app.services.ai_client import ai_available, generate_prompt

router = APIRouter(tags=["PROMPTS"])

_SEED_PATH = Path(__file__).parent.parent / "prompts" / "user_prompts.json"
_SEED_PROMPTS: dict[str, list[str]] = json.loads(_SEED_PATH.read_text())
DEFAULT_RECIPIENT = Query("other")


def _seed_prompt(recipient_type: str) -> str | None:
    candidates = _SEED_PROMPTS.get(recipient_type, [])
    if not candidates:
        candidates = _SEED_PROMPTS.get("other", [])
    if not candidates:
        return None
    return random.choice(candidates)


@router.get("/prompt", response_model=PromptResponse)
async def get_prompt(recipient_type: RecipientType = DEFAULT_RECIPIENT):
    if ai_available():
        ai_prompt = await generate_prompt(recipient_type)
        return PromptResponse(prompt=ai_prompt, recipient_type=recipient_type)

    seed_prompt = _seed_prompt(recipient_type)
    if seed_prompt:
        return PromptResponse(prompt=seed_prompt, recipient_type=recipient_type)

    fallback = await generate_prompt(recipient_type)
    return PromptResponse(prompt=fallback, recipient_type=recipient_type)
