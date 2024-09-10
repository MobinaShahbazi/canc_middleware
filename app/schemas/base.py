from fastapi import status
from pydantic import BaseModel
from humps import camel
from enum import Enum
from typing import Optional, Any


class BaseCustomModel(BaseModel):

    class Config:
        populate_by_name = True
        from_attributes = True


class BaseResponse(BaseModel):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[Any] = None

    class Config:
        populate_by_name = True
        from_attributes = True


class BaseResponseRecords(BaseModel):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[list[dict]] | None = None

    class Config:
        populate_by_name = True
        from_attributes = True


def to_camel(string):
    return camel.case(string)


class CamelCaseModel(BaseModel):

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class BaseResponseCamelCase(BaseResponse):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[Any] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class GridModel(BaseCustomModel):
    columns: Optional[list[str] | dict]
    rows: list[dict]

class GridResponse(BaseResponseCamelCase):
    body: GridModel | None = None
