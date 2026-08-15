from typing import Literal, Optional

from pydantic import BaseModel, Field

RecipientType = Literal["ex", "job", "past_self", "person_lost", "other"]

class PromptResponse(BaseModel):
    prompt: str
    recipient_type: RecipientType

class ReflectRequest(BaseModel):
    letter_text: str = Field(..., min_length=1, max_length=8000)
    recipient_type: RecipientType
    tone: Literal["gentle", "encouraging", "neutral"] = "gentle"


class ReflectResponse(BaseModel):
    reflection: str
    safe_to_release: bool
    resource_note: Optional[str] = None


class HealthResponse(BaseModel):
    status: Literal["ok", "degraded", "disabled"]
    ai_enabled: bool
    ai_reachable: bool
    ai_reason: Optional[str]