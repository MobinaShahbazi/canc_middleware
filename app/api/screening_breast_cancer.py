import json

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app import schemas
from app.templates import templates
from . import APIBaseClass
from app.settings import spiff_client, app_config
from fastapi.responses import HTMLResponse
from app.utilities.input_management import reform_info


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
        self.router.add_api_route(f'{prefix}/process-instances', self.get_process_instance, methods=['GET'],
                                  tags=['Breast Cancer Screening'],
                                  description='Initiates screening process from the start with a message.')

        self.modified_process_model_identifier = 'screenings:breast-cancer'

    def get_survey(self, request: Request):
        form_name = "breast-cancer-screening-v1.js"
        # form_name = 'test-form.js'
        form_submission_url = f"{app_config.app_url}/screenings/breast-cancer/v1/submit"
        return templates.TemplateResponse("form-submission.html",
                                          context={'request': request,
                                                   'form_name': form_name,
                                                   'form_submission_url': form_submission_url})

    def submit(self, request: schemas.FormBase) -> dict:
        obj_in_data = jsonable_encoder(request)
        result = self.start_bpmn(obj_in_data['survey_response'])
        return json.loads(result)

    def start_bpmn(self, input_obj):
        mw = spiff_client
        result_direct = mw.direct_call('start', {})
        instance_id = result_direct['process_instance']['id']

        result_ready = mw.trigger_process(instance_id)
        task_id = result_ready["results"][0]["id"]

        self_assessment_data = reform_info(input_obj)

        mw.put_data(self_assessment_data, instance_id, task_id)
        data = mw.get_task_data(instance_id, mw.get_end_event_id(instance_id))

        return json.dumps(data)

    def get_process_instance(self):
        results = spiff_client.get_process_instances(
            modified_process_model_identifier=self.modified_process_model_identifier
        )
        
        return results


router = BreastCancerScreening().router
