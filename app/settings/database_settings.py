import os
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):

    # TODO Can use PostgresDsn data type here but results in an error
    # SWH Database Configs
    db_name: str = 'middleware'
    db_base_url: str = "postgresql+psycopg2://postgres:1211381msh@host.docker.internal:5432"
    sqlalchemy_database_url: str = f'{db_base_url}/{db_name}'

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore"
    )
