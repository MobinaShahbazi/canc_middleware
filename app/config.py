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
    # if "ENV_FILE_PATH" in os.environ:
    #     access_token: str = os.getenv('ACCESS_TOKEN')
    #     base_url: str = os.getenv('BASE_URL')
    #     project_location: str = os.getenv('PROJECT_LOCATION')
    # else:
    access_token: str = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNwaWZmd29ya2Zsb3dfYmFja2VuZF9vcGVuX2lkIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvb3BlbmlkIiwiYXVkIjpbInNwaWZmd29ya2Zsb3ctYmFja2VuZCIsIkpYZVFFeG0wSmhRUEx1bWdIdElJcWY1MmJEYWxIejBxIl0sImlhdCI6MTcyNDA0ODc2NywiZXhwIjoxNzI0MjIxNTY4LCJzdWIiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5Ac3BpZmZ3b3JrZmxvdy5vcmciLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBZG1pbiJ9.CukXixVSNq_fZib-YCTn-B-FgAvwX-p1wprZ_MMh5iaOM5nSey83lkV_3vYTbL1ypozqaMnyNAsoDUsv8RLR87jbt3SsMyQUG4sFjYMZPGx2c8n0v2KcePtPRI8toxzjT7KkZ2vJcP1gqi4syBBDqrE0zDjW65ApYML8RaQLOiDF75f5m3Kh-obUn0quRb7aGJlFdKZx8DhUpHz8yvW4EpOyIU-NXCc2hN8qHteVfXoKzlR-2QrFnHV1oPecw9Iuhov6EpWZSTqO-GBB1BwPXLBa6yfD4SosFfscq9yZuzZmhZuqez_D-DJWdP0MRHpnEwoMmpsPli_3XsDWeM5mJg"
    base_url: str = "http://host.docker.internal:8000/v1.0"
    project_location: str = "demo:breast-cancer"


    # General application configs
    app_name: str = 'Middleware'
    app_version: str = '0.0.1'

    # TODO Can use PostgresDsn data type here but results in an error
    # SWH Database Configs
    db_name: str = 'middleware'
    # db_base_url: str = os.getenv('DB_BASE_URL')
    db_base_url: str = "postgresql+psycopg2://postgres:1211381msh@host.docker.internal:5432"
    sqlalchemy_database_url: str = f'{db_base_url}/{db_name}'


app_config = CommonSettings()
