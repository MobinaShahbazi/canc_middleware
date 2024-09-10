from fastapi import status
from pydantic import BaseModel
from humps import camel
from enum import Enum
from typing import Optional, Any

def to_camel(string):
    return camel.case(string)

class BaseResponse(BaseModel):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[Any] = None

    class Config:
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


