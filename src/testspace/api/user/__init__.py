from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from testspace.models.user import User
from typing import List, Optional
from uuid import UUID
from testspace.api import set_common_api
router = APIRouter(tags=["usermanagement"])

class UseConfig(BaseModel):
    class Config:
        orm_mode = True

class UserProp(UseConfig):
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

class UpdateUser(UseConfig):
    username: Optional[str] = None
    accountname: Optional[str] = None
    email: Optional[str] = None
    # password: Optional[str] = None

class PageDescription(BaseModel):
    total_items:int
    page_size: int
    max_index:int


set_common_api(router,User,PageDescription,UserProp,CreateUser,UpdateUser)

# @router.get("/page/description", response_model=PageDescription)
# def get_page_description(page_size:Optional[int]=None):
#     if page_size:
#         return User.page_description(page_size=page_size)
#     return User.page_description()

# @router.get("/page/{index}", response_model=List[UserProp])
# def get_page(index:int, page_size:Optional[int] = None):
#     if page_size:
#         return User.page(index,page_size=page_size)
#     return User.page(index)

# @router.get("/{uuid}", response_model=UserProp)
# def get_user(uuid: UUID):
#     return User.select_by_uuid(uuid)

# @router.post("/",status_code=201, response_model=UserProp)
# def create_user(item: CreateUser):
#     user = User(**item.dict())
#     return User.add(user)

# @router.put("/{uuid}", response_model=UserProp)
# def update_user(uuid:UUID,  item: UpdateUser):
#     return User.update_item(uuid, **item.dict())