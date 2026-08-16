from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = ""
    AI_ENABLED: bool = False

    AI_PROVIDER: str
    AI_MODEL: str
    AI_API_KEY: str

    REQUEST_TIMEOUT_SECONDS: int = 15
    ENVIRONMENT: str = "Development"

    model_config = ConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
