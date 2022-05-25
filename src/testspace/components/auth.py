from datetime import datetime, timedelta
from enum import Enum
from typing import Optional,Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Cookie, Depends, HTTPException, FastAPI, status, Request, Header
from fastapi.responses import Response

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel

from testspace.crud.user import R_get_user_by_email, R_get_user_by_name
from testspace.db.Session import  session
from testspace.log import logger
from testspace.config import SECRET_KEY
from . import current_user




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
class LoginType(str, Enum):
    email = "email"
    username ="username"
class LoginArgs(BaseModel):
    account:str
    password:str
    login_type:str

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_name(name:str):
    return R_get_user_by_name(session,name)
def get_user_by_email(mail:str):
    return R_get_user_by_email(session,mail)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(value: str, password: str, login_type="username"):
    if login_type == LoginType.username:
        user = get_user_by_name(value)
    elif login_type == LoginType.email:
        user = get_user_by_email(value)
    else:
        raise Exception(f"unsupported login_type {login_type}")
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(access_token: Optional[str]= Cookie(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(payload)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_name(token_data.username)
    if user is None:
        raise credentials_exception
    return user




def set_auth(app:FastAPI):
    @app.post("/login", tags=["user login"], response_model=Token)
    async def login(response: Response, login_data: LoginArgs):
        user = authenticate_user(login_data.account, login_data.password, login_data.login_type)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect account or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}





    @app.middleware("http")
    async def auth_get(request:Request, call_next):
        '''  '''
        logger.info("[pink bold]{}[/] request  - {} {} ".format(
            current_user.username if current_user.get() else "",
            request.method,
            request.url,
            ),extra={"markup": True})
        path = request.url.path
        if path not in ["/redoc","/docs","/index","/openapi.json","/login","/"] and request.method != "OPTIONS":
            # pass
            try:
                token = request.cookies.get("access_token")
                if token is None:
                    token = request.headers.get("access_token",default=None)
                user = await get_current_user(token)
                current_user.set(user)
                logger.info(f"access token:  {request.cookies.get('access_token')} ")
            except HTTPException as e:
                return Response(e.detail,status_code=e.status_code,headers=e.headers )  # type: ignore
        response:Response = await call_next(request)
        logger.info("[pink bold]{}[/] response  - {} {} {}".format(
            current_user.username if current_user.get() else "",
            request.method,
            request.url,
            response.status_code
            ),extra={"markup": True})
        return response