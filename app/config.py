import os

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

# if "ENV_FILE_PATH" in os.environ:
#     load_dotenv(os.environ["ENV_FILE_PATH"], override=True)
# else:
#     load_dotenv()


class CommonSettings(BaseSettings):
    # Basic application configs
    app_port: int = 42420

    # access_token: str = os.getenv('ACCESS_TOKEN')
    # base_url: str = os.getenv('BASE_URL')
    # project_location: str = os.getenv('PROJECT_LOCATION')

    access_token: str = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNwaWZmd29ya2Zsb3dfYmFja2VuZF9vcGVuX2lkIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvb3BlbmlkIiwiYXVkIjpbInNwaWZmd29ya2Zsb3ctYmFja2VuZCIsIkpYZVFFeG0wSmhRUEx1bWdIdElJcWY1MmJEYWxIejBxIl0sImlhdCI6MTcyNDE2MjY2MCwiZXhwIjoxNzI0MzM1NDYxLCJzdWIiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5Ac3BpZmZ3b3JrZmxvdy5vcmciLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBZG1pbiJ9.fZ-YmKD-9hqrdRoispfH9AOuTpbMa0hgesYJtuvnvHxRpNIDAbrHFSw2-Cch_yRW1pTHpB29HedmLGarvV26P6loyDDw5UMF9GZd8Xjk5aAm4XIVYoR4TXbttfOJq5PSpUn4qpteaPpiMbwxZfLnlwOHOKj4U-AG76CDCz_Orw4asdeL2W1G480U3c6CDwXKVnMuVPPBo_mGUCXAbeK5tn_fXnCkdJqLLfho30334IsWQqKmcq5VvuQYpf9h8PqRM4E1qdoHW20siPyGaoWVxgDx12JHaw9tckupZFM12lDiB6xJNUbYZjTNnMTqbsvv8Eqf6LUEvRFob7pTn2IiMA"
    # base_url: str = "http://host.docker.internal:8000/v1.0"
    base_url: str = "http://localhost:8000/v1.0"
    project_location: str = "demo:breast-cancer"

    # General application configs
    app_name: str = 'Development'
    app_version: str = '0.0.1'

    # TODO Can use PostgresDsn data type here but results in an error
    # SWH Database Configs
    db_name: str = 'middleware'
    # sqlalchemy_database_url: str = f'postgresql+psycopg2://postgres:1211381msh@127.0.0.1:5432/{db_name}'
    sqlalchemy_database_url: str = f'postgresql+psycopg2://postgres:1211381msh@host.docker.internal:5432/{db_name}'


app_config = CommonSettings()
