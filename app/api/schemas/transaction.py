from typing import Optional, List,Dict, Union
from pydantic import BaseModel,StrictStr, StrictBool, StrictFloat, validator
from datetime import date
import utils.auth as auth_utils

class RequestTopup(BaseModel):
    nominal: StrictFloat
    

class ResponseTopupItem(BaseModel):
    credit: StrictFloat


class ResponseTopup(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseTopupItem