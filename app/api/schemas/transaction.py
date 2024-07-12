from typing import Optional, List,Dict, Union
from pydantic import BaseModel,StrictStr, StrictBool, StrictFloat, validator
from datetime import date
import utils.auth as auth_utils

class RequestTopup(BaseModel):
    nominal: StrictFloat
    @validator("nominal")
    def nominal_handler(cls, value):
        if value <= 0:
            raise ValueError("nominal cannot be 0 or lower than 0")
        return value
    

class ResponseTopupItem(BaseModel):
    credit: StrictFloat


class ResponseTopup(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseTopupItem