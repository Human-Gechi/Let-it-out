import time

import requests
from groq import Groq, GroqError

from backend.app.config import get_settings
from backend.app.prompts.system_prompts import (
    PROMPT_SYSTEM_PROMPT,
    REFLECTION_SYSTEM_PROMPT,
)
from backend.app.schemas import HealthResponse

settings = get_settings()


_client: Groq | None = None
if settings.AI_API_KEY:
    _client = Groq(api_key=settings.AI_API_KEY)

_CACHE_TTL_SECONDS: float = 60.0
_last_check_timestamp: float = 0.0
_cached_status: HealthResponse | None = None


def _ai_available() -> bool:
    return settings.AI_ENABLED and _client is not None


def _fallback_reflection() -> str:
    return (
        "Thank you for putting this into words. Whatever happens to this "
        "letter next, you've already done the harder part — naming it."
    )


def _fallback_prompt() -> str:
    return "What's something you never got the chance to say?"


async def generate_reflection(text: str, recipient_type: str, tone: str) -> str:
    if not _ai_available():
        return _fallback_reflection()

    try:
        response = _client.chat.completions.create(
            model=settings.AI_MODEL,
            max_tokens=200,
            messages=[
                {"role": "system", "content": REFLECTION_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Recipient type: {recipient_type}. Desired tone: {tone}.\n\n"
                        f"Letter:\n{text}"
                    ),
                },
            ],
        )
        return response.choices[0].message.content
    except GroqError:
        return _fallback_reflection()


async def generate_prompt(recipient_type: str) -> str:
    if not _ai_available():
        return _fallback_prompt()

    try:
        response = _client.chat.completions.create(
            model=settings.AI_MODEL,
            max_tokens=60,
            messages=[
                {"role": "system", "content": PROMPT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Recipient type: {recipient_type}"},
            ],
        )
        return response.choices[0].message.content
    except GroqError:
        return _fallback_prompt()


def check_ai_status() -> HealthResponse:
    global _last_check_timestamp, _cached_status

    if not settings.AI_ENABLED:
        return HealthResponse(
            status="disabled",
            ai_enabled=False,
            ai_reachable=False,
            ai_reason="AI feature is disabled in settings",
        )

    if not settings.AI_API_KEY or _client is None:
        return HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason="AI API key is missing or empty",
        )

    now = time.monotonic()
    if (
        _cached_status is not None
        and (now - _last_check_timestamp) < _CACHE_TTL_SECONDS
    ):
        return _cached_status

    try:
        client = Groq(api_key=settings.AI_API_KEY)

        client.chat.completions.create(
            model=settings.AI_MODEL,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=1,
        )

        status = HealthResponse(
            status="ok",
            ai_enabled=True,
            ai_reachable=True,
            ai_reason=None,
        )

    except requests.RequestException:
        status = HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason="Network error communicating with provider",
        )
    except TimeoutError:
        status = HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason="Request to provider timed out",
        )
    except Exception as exc:
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        status = HealthResponse(
            status="degraded",
            ai_enabled=True,
            ai_reachable=False,
            ai_reason=f"Unexpected error communicating with provider: {exc}",
        )
    _last_check_timestamp = now
    _cached_status = status
    return status
