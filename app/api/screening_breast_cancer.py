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
        prefix = '/screenings/breast-cancer/v1'
        self.router.add_api_route(f'{prefix}/survey', self.get_survey, methods=['GET'],
                                  tags=['Breast Cancer Screening'], response_class=HTMLResponse,
                                  description='Initiates screening process from the start with a message.')
        self.router.add_api_route(f'{prefix}/submit', self.submit, methods=['POST'],
                                  tags=['Breast Cancer Screening'],
                                  description='Initiates screening process from the start with a message.')

        self.modified_process_model_identifier = 'cancer-breast-screening:breast-cancer-screening-self-report'

    def get_survey(self, request: Request):
        form_name = "breast-cancer-screening-v1.js"
        form_submission_url = "http://localhost:42420/screenings/breast-cancer/v1/submit"
        return templates.TemplateResponse("form-submission.html",
                                          context={'request': request,
                                                   'form_name': form_name,
                                                   'form_submission_url': form_submission_url})

    def submit(self, request: schemas.FormBase):
        mw = spiff_client
        obj_in_data = jsonable_encoder(request)
        result = mw.direct_call('screening-breast-cancer-self-report', obj_in_data['survey_response'])
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
