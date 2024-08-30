import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):

    service_base_dir: str = os.getcwd()
    service_log_level: int = logging.INFO

    # Basic application configs
    app_port: int = 42420

    # General application configs
    app_name: str = 'Cancer Screening Middleware'
    app_version: str = '0.0.1'
    app_description: str = 'Middleware services for cancer screening'
    app_summary: str = ''

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )
