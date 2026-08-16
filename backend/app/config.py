from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

DEFAULT_ALLOWED_ORIGINS = "http://127.0.0.1:3000,http://localhost:3000"


class Settings(BaseSettings):
    APP_NAME: str = ""
    AI_ENABLED: bool = False

    AI_PROVIDER: str = "groq"
    AI_MODEL: str = "llama-3.3-70b-versatile"
    AI_API_KEY: str = ""
    ALLOWED_ORIGINS: str = DEFAULT_ALLOWED_ORIGINS

    REQUEST_TIMEOUT_SECONDS: int = 15
    ENVIRONMENT: str = "Development"

    model_config = ConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        configured = self.ALLOWED_ORIGINS.strip() or DEFAULT_ALLOWED_ORIGINS
        return [origin.strip() for origin in configured.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
