from fastapi import APIRouter, Depends

from backend.app.schemas import ReflectRequest, ReflectResponse
from backend.app.services.ai_client import generate_reflection
from backend.app.services.ratelimit import rate_limit_dependency
from backend.app.services.safety import CRISIS_NOTE, flag_risk

router = APIRouter(tags=["REFLECT"])


@router.post(
    "/reflect",
    response_model=ReflectResponse,
    dependencies=[Depends(rate_limit_dependency(10, 60))],
)
async def reflect(payload: ReflectRequest) -> ReflectResponse:
    if flag_risk(payload.letter_text):
        return ReflectResponse(
            reflection=(
                "It sounds like you're carrying something very heavy right now. "
                "That matters more than this letter does."
            ),
            safe_to_release=False,
            resource_note=CRISIS_NOTE,
        )

    reflection_text = await generate_reflection(
        text=payload.letter_text,
        recipient_type=payload.recipient_type,
        tone=payload.tone,
    )

    return ReflectResponse(
        reflection=reflection_text,
        safe_to_release=True,
        resource_note=None,
    )
