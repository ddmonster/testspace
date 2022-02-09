from sqlalchemy import Column, Integer, String, DateTime, Boolean
from testspace.db.base_class import Base
from testspace.db.session import SessionLocal
from testspace.utils.gen import uuid_v4, curtime

class User(Base):

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
    


    @classmethod
    def select_all(cls):
        session = SessionLocal()
        return session.query(User).all()


    @classmethod
    def select_by_id(cls, id):
        session = SessionLocal()
        return session.query(User).filter_by(id=id).first()
    
    @classmethod
    def add(cls, user):
        session = SessionLocal()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def __repr__(self):
        return "<User {}>".format(self.username)
