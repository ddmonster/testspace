from sqlalchemy import Column, Integer, String, DateTime, Boolean
from . import Base, TableCRUD
from testspace.utils.gen import uuid_v4, curtime




class User(Base,TableCRUD):

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False,default=uuid_v4)
    username = Column(String, index=True, unique=True)
    accountname = Column(String, index=True)
    password = Column(String)
    email = Column(String, index=True, unique=True)
    active = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=curtime)
    updated_at = Column(DateTime, default=curtime, onupdate=curtime)

    def __repr__(self):
        return "<User {}>".format(self.username)