from pydantic import BaseModel
from typing import Optional
from . import CommonProps
class UseConfig(BaseModel):
    class Config:
        orm_mode = True

class UserProps(UseConfig,CommonProps):
    username: str
    accountname: str
    email: str
    active: bool
    admin: bool
    avatar:str
    password: Optional[str]

class CreateUser(UseConfig):
    username: str
    accountname: str
    email: str
    password: str
    admin: Optional[bool]
    avatar:Optional[str]

class UpdateUser(UseConfig):
    username: Optional[str]
    accountname: Optional[str] 
    email: Optional[str] 
    avatar:Optional[str]
    password: Optional[str]
    admin: Optional[bool]