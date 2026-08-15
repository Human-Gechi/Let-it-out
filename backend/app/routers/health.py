from fastapi import APIRouter
from backend.app.schemas import HealthResponse
from backend.app.services.ai_client import check_ai_status

router = APIRouter(tags=["HEALTH"], prefix="/api/v1")

@router.get("/health", response_model=HealthResponse)
async def health():
    ai_status = check_ai_status()

    return HealthResponse(
        status="ok",
        ai_enabled=ai_status.ai_enabled,
        ai_reachable=ai_status.ai_reachable,
        ai_reason=ai_status.ai_reason
    )