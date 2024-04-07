from typing import Optional, List,Dict, Union
from pydantic import BaseModel,StrictStr, StrictBool, StrictFloat, validator
from datetime import date
import utils.auth as auth_utils


class RequestDaftar(BaseModel):
    username: StrictStr
    password: StrictStr
    nama: StrictStr
    role: StrictStr
    email: StrictStr
    @validator("username")
    def username_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Username cannot be an empty string")
        return value
    @validator("nama")
    def nama_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Nama cannot be an empty string")
        return value
    @validator("password")
    def validate_password(cls, value):
        if not auth_utils.validate_password(value):
            raise ValueError("Password should have a minimum of 6 digits and must include at least 1 symbol, 1 number, and 1 uppercase letter")
        return value
    @validator("email")
    def validate_email(cls, value):
        if not auth_utils.validate_email(value):
            raise ValueError("Wrong email format")
        return value
    @validator("role")
    def validate_role(cls, value):
        if value.lower() not in ["admin", "cust"]:
            raise ValueError("Role must be either 'admin' or 'cust'")
        return value
    
class ResponseDaftarItem(BaseModel):
    success: StrictBool


class ResponseDaftar(BaseModel):
    resp_msg: StrictStr
    resp_data: None

# class RequestUser(BaseModel):
#     username: str

class ResponseUserItem(BaseModel):
    username: str
    nama: str
    role: str
    email: str
    created_at: str
    updated_at: Optional[str]
    is_deleted: bool

class ResponseUser(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseUserItem

class ResponseUsers(BaseModel):
    resp_msg: StrictStr
    resp_data: List[ResponseUserItem]

class RequestTopup(BaseModel):
    credit: StrictFloat
    @validator("credit")
    def validate_credit(cls, value):
        if value <= 0:
            raise ValueError("Credit must be greater than 0")
        return value

class ResponseTopupItem(BaseModel):
    saldo: StrictFloat
class ResponseTopup(BaseModel):
    resp_msg: StrictStr
    resp_data: ResponseTopupItem
