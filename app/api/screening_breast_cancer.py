from fastapi.encoders import jsonable_encoder
from app import schemas
from . import APIBaseClass
from app.settings import spiff_client


class BreastCancerScreening(APIBaseClass):

    def __init__(self):
        super().__init__()
        self.router.add_api_route('/part1', self.create, methods=['POST'], tags=['Breast Cancer Screening'],
                                  description='Initiates screening process from the start with a message.')
        self.router.add_api_route('/part2', self.create2, methods=['POST'], tags=['Breast Cancer Screening'],
                                  description='Calls for patient consent')
        self.router.add_api_route('/part3', self.create3, methods=['POST'], tags=['Breast Cancer Screening'],
                                  description='Initiates screening process from the start with a message.')
        self.router.add_api_route('/process-instances', self.create_process_instance, methods=['POST'],
                                  tags=['Breast Cancer Screening'],
                                  description='Creates a process instance')

        self.modified_process_model_identifier = 'cancer-breast-screening:breast-cancer-screening-self-report'

    def create(self, request_body: schemas.FormCreate):
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

    def get_process_instances(self):
        results = spiff_client.get_process_instances(
            modified_process_model_identifier=self.modified_process_model_identifier
        )
        return results


router = BreastCancerScreening().router
