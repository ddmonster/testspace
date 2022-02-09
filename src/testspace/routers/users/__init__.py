from fastapi import APIRouter
from pydantic import BaseModel
from testspace.models.user import User
from typing import List


router = APIRouter(tags=["usermanagement"])

class UseConfig(BaseModel):
    class Config:
        orm_mode = True

class UserProp(UseConfig):
    uuid:str
    username: str
    accountname: str
    email: str

class CreateUser(UseConfig):
    username: str
    accountname: str
    email: str
    

@router.get("/", response_model=List[UserProp])
def read_items():
    return User.select_all()


@router.get("/{user_id}", response_model=UserProp)
def read_item(user_id: str):
    return User.select_by_id(user_id)

@router.post("/", response_model=UserProp)
def create_item(item: CreateUser):
    user = User(**item.dict())
    return User.add(user)
