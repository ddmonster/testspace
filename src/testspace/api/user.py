import asyncio
from datetime import timedelta
from fastapi import APIRouter, Cookie, Depends, Header, Response
from testspace.models.user import User
from testspace.api import set_page_enable_api
from passlib.context import CryptContext
from testspace.schemas.user import *
from testspace.crud.user import C_create_user
from testspace.db.Session import session
from testspace.components.auth import current_user, pwd_context
                                                


router = APIRouter(tags=["usermanagement"])
set_page_enable_api(router, User, UserProps)


@router.post("/", status_code=201, response_model=UserProps)
async def create_user(item: CreateUser):
        item.password = pwd_context.hash(item.password)
        return C_create_user(session, item)



@router.get("/me", response_model=UserProps)
async def read_current_user():
    '''  return current login user '''
    if current_user is not None:
        return current_user
