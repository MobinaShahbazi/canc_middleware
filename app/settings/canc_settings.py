from pydantic_settings import BaseSettings, SettingsConfigDict


class CancConnectorSettings(BaseSettings):

    canc_base_api_url: str | None = None
    canc_base_url: str | None = None
    canc_user: str | None = None
    canc_password: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )
