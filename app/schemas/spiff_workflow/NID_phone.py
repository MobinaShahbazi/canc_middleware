from typing import Dict, Any, Optional, Type
from pydantic import BaseModel


class Info(BaseModel):

    NID: str
    phone: str


class InfoCreate(Info):
    pass

class InfoUpdate(Info):
    pass

