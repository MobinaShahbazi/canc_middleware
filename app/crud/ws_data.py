from typing import Type
from app.crud.base import CRUDBase
from fastapi import HTTPException
from app import models, schemas
from sqlalchemy.orm import Session
from sqlalchemy import update, insert, delete
from .base import ModelType, CreateSchemaType, UpdateSchemaType
from fastapi.encoders import jsonable_encoder
# from . import workspaces_crud


class WSDataCRUD(CRUDBase[models.WSData, schemas.FormCreate, schemas.FormUpdate]):

    def create_by_workspace_code(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:


        return None


ws_data_crud = WSDataCRUD(models.WSData)
