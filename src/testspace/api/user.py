from fastapi import APIRouter,Depends
from testspace.models.user import User,UserGroup
from testspace.utils.pydantictools import Omit                                          
from testspace.db.session import engine
from sqlmodel import Session,select
from uuid import UUID
from typing import TypedDict
from testspace.components.auth import get_password_hash,oauth2_scheme
router = APIRouter(tags=["usermanagement"],dependencies=[Depends(oauth2_scheme)])

UserModel = Omit["UserModel", User, "password"]
@router.post("/",response_model=UserModel)
async def add_user(user: Omit["UserCreate",User,"uuid","id"]):
    new_user  = User(**user.dict(exclude_unset=True))
    new_user.password =  get_password_hash(new_user.password)
    with Session(engine) as s:
        s.add(new_user)
        s.commit()
        s.refresh(new_user)
        return new_user

@router.post("/group",response_model=UserGroup)
async def add_group(group_add: Omit["UserGroupAdd",UserGroup,"uuid","id"]):
    user_group = UserGroup(**group_add.dict(exclude_unset=True))
    with Session(engine) as s:
        s.add(user_group)
        s.commit()
        s.refresh(user_group)
        return user_group
    
@router.post("/{user_id}",response_model=TypedDict("UserWithGroups",{
    "user":User,
    "groups":list[UserGroup]
}))
async def add_group_to_user(group_id:UUID,user_id:UUID):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.uuid == user_id)).one()  # type: ignore
        group =  s.exec(select(UserGroup).where(UserGroup.uuid == group_id)).one()  # type: ignore
        user.groups.append(group)
        s.add(user)
        s.commit()
        print(user.groups)
        return {"user":user,"groups":user.groups}