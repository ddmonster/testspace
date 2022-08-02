
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import sqlalchemy
from sqlmodel import select,Session
from pydantic import BaseModel
from testspace.config import TomlConfig
from testspace.models.user import User
from sqlalchemy.engine.base import Engine

from passlib.context import CryptContext
__all__ = ["get_password_hash","verify_password","authenticate_user","setup_auth_component","oauth2_scheme"]


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str
def verify_password(plain_password:str, hashed_password:str):
    return crypt_context.verify(plain_password, hashed_password)
def get_password_hash(password:str):
    return crypt_context.hash(password.encode("utf-8"))
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(engine:Engine,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(engine, username=username)
    if user is None:
        raise credentials_exception
    return user
def get_user(engine:Engine, username: str):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == username)).first()
        if user:
            return user
def authenticate_user(engine:Engine,username: str, password: str):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == username)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
def setup_auth_component(app:FastAPI,engine:Engine):

    @app.post("/token", response_model=Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(engine,form_data.username, form_data.password)
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
        return {"access_token": access_token, "token_type": "bearer"}
    