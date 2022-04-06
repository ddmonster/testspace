from typing import Union
from sqlalchemy.orm import Session
from testspace.schemas.user import *
from testspace.models.user import User


def C_create_user(s:Session, create_schema:CreateUser) -> UserProps:
    user = User(**create_schema.dict())
    s.add(user)
    s.commit()
    return user

def R_get_user_by_name(s:Session, name:str) -> Union[None,UserProps]:
    return s.query(User).filter_by(username=name).first()

def R_get_user_by_email(s:Session, mail:str) -> Union[None,UserProps]:
    return s.query(User).filter_by(mail=mail).first()