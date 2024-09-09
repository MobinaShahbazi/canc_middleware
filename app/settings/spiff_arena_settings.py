import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class SpiffArenaConnectorSettings(BaseSettings):

    spiff_arena_base_url: str = "http://host.docker.internal:8000"
    spiff_arena_base_api_url: str = "http://host.docker.internal:8000/v1.0"
    spiff_arena_token: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )
