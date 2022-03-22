from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Cookie, Depends, HTTPException, FastAPI, status, Request, Header
from fastapi.responses import Response

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel

from testspace.crud.user import R_get_user_by_name
from testspace.db.session import  openSession
from testspace.schemas.user import UserProps
from testspace.log import logger

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


SECRET_KEY = "5aaca26c7bb7d1d8d2312498006db19cfe3953152a2541ab725ce8098c7d506c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_name(name:str):
    with openSession() as s:
        return R_get_user_by_name(s,name)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = get_user_by_name(username)
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

async def get_current_user(auth_token: Optional[str]= Cookie(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if auth_token is None:
        raise credentials_exception
   
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
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
    @app.post("/token",tags=["login"])
    async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        response.set_cookie(key="auth_token",value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}


    @app.get("/users/me", response_model=UserProps)
    async def read_users_me(authorized_user: Optional[str] = Header(None)):
        '''  return current login user '''
        logger.info(authorized_user)
        return get_user_by_name(authorized_user)



    @app.middleware("http")
    async def auth_get(request:Request, call_next):
        '''extract user from incomming request and set header "authorized-user: [username]"   '''
        path = request.url.path
        if path not in ["/redoc","/docs","/index","/openapi.json","/token","/"]:
            # pass
            try:
                user = await get_current_user(request.cookies.get("auth_token"))
                logger.info(f"{request.cookies.get('auth_token')} >>>>>>>>>")
            except HTTPException as e:
                return Response(e.detail,status_code=e.status_code,headers=e.headers)
            request.headers.__dict__["_list"].append(("authorized-user".encode(),f"{user.username}".encode()))
            logger.info(f"{user.username} >>>>>>>>>")
        response = await call_next(request)

        return response