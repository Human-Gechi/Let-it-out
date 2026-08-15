import json
import random
from pathlib import Path

from fastapi import APIRouter, Depends, Query

from backend.app.schemas import PromptResponse, RecipientType
from backend.app.services.ai_client import generate_prompt
from backend.app.services.ratelimit import rate_limit_dependency

router = APIRouter(tags=["PROMPTS"])

_SEED_PATH = Path(__file__).parent.parent / "prompts" / "user_prompts.json"
_SEED_PROMPTS: dict[str, list[str]] = json.loads(_SEED_PATH.read_text())
DEFAULT_RECIPIENT = Query("other")


@router.get(
    "/prompt",
    response_model=PromptResponse,
    dependencies=[Depends(rate_limit_dependency(10, 60))],
)
async def get_prompt(recipient_type: RecipientType = DEFAULT_RECIPIENT):
    candidates = _SEED_PROMPTS.get(recipient_type, [])

    if not candidates:
        candidates = _SEED_PROMPTS.get("other", [])

    if not candidates:
        prompt_text = await generate_prompt(recipient_type)
        return PromptResponse(prompt=prompt_text, recipient_type=recipient_type)

    return PromptResponse(
        prompt=random.choice(candidates),
        recipient_type=recipient_type,
    )
