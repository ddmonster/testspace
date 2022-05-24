from email.policy import default
from sqlalchemy import Column, String, Boolean

from . import Base, BaseMixin
from .redbtype import UUIDList
class User(Base, BaseMixin):

    username = Column(String, index=True, unique=True)
    accountname = Column(String, index=True)
    password = Column(String)
    email = Column(String, index=True)
    active = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    avatar = Column(String,default="")
    group = UUIDList()
    def __repr__(self):
        return "<User {}>".format(self.username)