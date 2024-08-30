# import common endpoints here
from .api_base import APIBaseClass
from .general import AppInfo

# import api specific endpoints here
from .general import router as app_base_api
from .screening_breast_cancer import router as breast_cancer_screening_api

routers = (
    app_base_api,
    breast_cancer_screening_api
)