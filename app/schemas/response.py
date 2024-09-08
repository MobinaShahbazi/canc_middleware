class BaseResponse(BaseModel):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[Any] = None

    class Config:
        populate_by_name = True
        from_attributes = True


def to_camel(string):
    return camel.case(string)


class BaseResponseCamelCase(BaseResponse):

    status: str
    message_code: int
    message: Optional[str | None] = None
    body: Optional[Any] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


