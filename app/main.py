import os
import uvicorn
from fastapi import APIRouter, FastAPI
from app.settings import app_config
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware

from app.api import routers


# Initialize the application
app = FastAPI(
    title=app_config.app_name,
    version=app_config.app_version,
    description=app_config.app_description,
    summary=app_config.app_summary
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set templating preferences
script_dir = os.path.dirname(__file__)
app.mount('/static', StaticFiles(directory=os.path.join(script_dir, "static/")), name='static')

# add routers automatically from api module
for x_router in routers:
    if x_router and isinstance(x_router, APIRouter):
        app.include_router(x_router)
        continue
    print(f'routers expected an instance of APIRouter but get {type(x_router)}')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=app_config.app_port)
