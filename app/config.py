import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

if "ENV_FILE_PATH" in os.environ:
    load_dotenv(os.environ["ENV_FILE_PATH"], override=True)
else:
    load_dotenv()


class CommonSettings(BaseSettings):
    # Basic application configs
    app_port: int = 42420

    access_token: str = os.getenv('ACCESS_TOKEN')
    base_url: str = os.getenv('BASE_URL')
    project_location: str = os.getenv('PROJECT_LOCATION')

    # General application configs
    app_name: str = 'Development'
    app_version: str = '0.0.1'

    # TODO Can use PostgresDsn data type here but results in an error
    # SWH Database Configs
    db_name: str = 'middleware'
    sqlalchemy_database_url: str = f'postgresql+psycopg2://postgres:1211381msh@127.0.0.1:5432/{db_name}'


app_config = CommonSettings()
