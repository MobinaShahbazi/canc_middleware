from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import schemas
from . import APIBaseClass

from app.utility.services import Middleware


class WSDataDAO(APIBaseClass):

    def __init__(self):
        super().__init__()
        self.router.add_api_route('/part1', self.create, methods=['POST'])
        self.router.add_api_route('/part2', self.create2, methods=['POST'])
        self.router.add_api_route('/part3', self.create3, methods=['POST'])

    def create(self, request_body: schemas.FormCreate, db: Session = Depends(get_db)):

        mw = Middleware()
        obj_in_data = jsonable_encoder(request_body)
        mw.direct_call('msg', obj_in_data)
        result = mw.request_result
        return result
    def create2(self, request_body: schemas.PatientConsentCreate, db: Session = Depends(get_db)):

        mw = Middleware()
        obj_in_data = jsonable_encoder(request_body)
        result = mw.direct_call('patient_consent', obj_in_data)
        return result
    def create3(self, request_body: schemas.InfoCreate, db: Session = Depends(get_db)):

        mw = Middleware()
        obj_in_data = jsonable_encoder(request_body)
        result = mw.direct_call('get_NID_phone', obj_in_data)
        return result
