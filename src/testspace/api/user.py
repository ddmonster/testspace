from datetime import timedelta
from fastapi import APIRouter, Cookie, Depends, Header, Response
from testspace.models.user import User
from testspace.api import set_page_enable_api
from passlib.context import CryptContext
from testspace.schemas.user import *
from testspace.crud.user import C_create_user
from testspace.db.session import get_db, Session
from testspace.components.auth import Token, LoginArgs, authenticate_user, HTTPException, status,\
                                            ACCESS_TOKEN_EXPIRE_MINUTES,\
                                            create_access_token,\
                                                get_current_user
                                                


router = APIRouter(tags=["usermanagement"])


set_page_enable_api(router, User, UserProps)


@router.post("/", status_code=201, response_model=UserProps)
async def create_user(item: CreateUser, session: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    item.password = pwd_context.hash(item.password)
    return C_create_user(session, item)



@router.get("/user/me", response_model=UserProps)
async def read_users_me(access_token: Optional[str] = Header(None), access_token_cookies: Optional[str] = Cookie(None, alias="access_token")):
    '''  return current login user '''
    _access_token = ""
    if access_token is not None:
        _access_token = access_token
    elif access_token_cookies is not None:
        _access_token = access_token_cookies
    user = await get_current_user(_access_token)
    return user
