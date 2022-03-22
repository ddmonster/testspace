from fastapi import APIRouter, Depends
from testspace.models.user import User
from testspace.api import set_page_enable_api
from passlib.context import CryptContext
from testspace.schemas.user import *;
from testspace.crud.user import C_create_user
from testspace.db.session import get_db, Session


router = APIRouter(tags=["usermanagement"])




set_page_enable_api(router,User,UserProps)

@router.post("/",status_code=201, response_model=UserProps)
async def create_user(item: CreateUser,session:Session = Depends(get_db)):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        item.password = pwd_context.hash(item.password)
        return C_create_user(session, item)