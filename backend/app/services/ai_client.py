import time
from typing import Optional

from groq import Groq

from backend.app.config import get_settings
from backend.app.schemas import HealthResponse

_CACHE_TTL_SECONDS: float = 60.0
_last_check_timestamp: float = 0.0
_cached_status: Optional[HealthResponse] = None

settings = get_settings()

def check_ai_status() -> HealthResponse:
    global _last_check_timestamp, _cached_status



    if not settings.AI_ENABLED:
        return HealthResponse(
            status="disabled",
            ai_enabled=False,
            ai_reachable=False,
            ai_reason="AI feature is disabled in settings",
        )

    api_key = settings.AI_API_KEY
    if not api_key:
        return HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason="AI API key is missing or empty",
        )

    now = time.monotonic()
    if _cached_status is not None and (now - _last_check_timestamp) < _CACHE_TTL_SECONDS:
        return _cached_status

    model = settings.AI_MODEL

    try:
        client = Groq(api_key=api_key)

        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )

        status = HealthResponse(
            status="ok",
            ai_enabled=True,
            ai_reachable=True,
            ai_reason=None,
        )

    except Exception:
        status = HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason="Unexpected error communicating with Groq",
        )

    _last_check_timestamp = now
    _cached_status = status
    return status

