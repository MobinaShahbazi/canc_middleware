from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.templates import templates
from . import APIBaseClass
from app.settings import spiff_client
from fastapi.responses import HTMLResponse


class BreastCancerScreening(APIBaseClass):

    def __init__(self):
        super().__init__()
        self.router.add_api_route('/breast-cancer-screening', self.get_survey, methods=['GET'],
                                  tags=['Breast Cancer Screening'], response_class=HTMLResponse,
                                  description='Initiates screening process from the start with a message.')
        self.router.add_api_route('/submit', self.submit, methods=['POST'], tags=['Breast Cancer Screening'],
                                  description='Initiates screening process from the start with a message.')

        self.modified_process_model_identifier = 'cancer-breast-screening:breast-cancer-screening-self-report'

    def get_survey(self, request: Request):
        return templates.TemplateResponse("breast-cancer-screening.html", context={'request': request})

    def submit(self, request_body: schemas.FormCreate):
        mw = spiff_client
        obj_in_data = jsonable_encoder(request_body)
        mw.direct_call('msg', obj_in_data)
        result = mw.request_result
        return result

    def create2(self, request_body: schemas.PatientConsentCreate):
        mw = spiff_client
        obj_in_data = jsonable_encoder(request_body)
        result = mw.direct_call('patient_consent', obj_in_data)
        return result

    def create3(self, request_body: schemas.InfoCreate):
        mw = spiff_client
        obj_in_data = jsonable_encoder(request_body)
        result = mw.direct_call('get_NID_phone', obj_in_data)
        return result

    def create_process_instance(self):
        results = spiff_client.get_process_instances(
            modified_process_model_identifier=self.modified_process_model_identifier
        )
        return results


router = BreastCancerScreening().router
