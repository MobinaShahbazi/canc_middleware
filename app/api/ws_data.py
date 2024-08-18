from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import schemas
from . import APIBaseClass

from app.utility.middleware import Middleware


class WSDataDAO(APIBaseClass):

    def __init__(self):
        super().__init__()
        self.router.add_api_route('/data', self.create, methods=['POST'])

    def create(self, request_body: schemas.FormCreate, db: Session = Depends(get_db)):

        mw = Middleware()
        print(type(request_body))
        obj_in_data = jsonable_encoder(request_body)
        result = mw.get_result(obj_in_data)
        return result

