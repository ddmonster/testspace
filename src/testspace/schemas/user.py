

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
    created_at: datetime
    updated_at: datetime

class CreateUser(UseConfig):
    username: str
    accountname: str
    email: str
    password: str
    admin: Optional[bool]

class UpdateUser(UseConfig):
    username: Optional[str] = None
    accountname: Optional[str] = None
    email: Optional[str] = None