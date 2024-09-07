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

        self.modified_process_model_identifier = 'screenings:breast-cancer'

    def get_survey(self, request: Request):
        form_name = "breast-cancer-screening-v1.js"
        # form_name = 'test-form.js'
        form_submission_url = "http://localhost:42420/screenings/breast-cancer/v1/submit"
        return templates.TemplateResponse("form-submission.html",
                                          context={'request': request,
                                                   'form_name': form_name,
                                                   'form_submission_url': form_submission_url})

    def submit(self, request: schemas.FormBase) -> dict:
        mw = spiff_client
        obj_in_data = jsonable_encoder(request)
        result = mw.start_bpmn(obj_in_data['survey_response'])
        return result

    def create_process_instance(self):
        results = spiff_client.get_process_instances(
            modified_process_model_identifier=self.modified_process_model_identifier
        )
        return results


router = BreastCancerScreening().router
