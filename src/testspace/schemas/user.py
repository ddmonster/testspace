

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
class UseConfig(BaseModel):
    class Config:
        orm_mode = True

class UserProps(UseConfig):
    uuid:UUID
    username: str
    accountname: str
    email: str
    active: bool
    admin: bool
    avatar:str
    created_at: datetime
    updated_at: datetime

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