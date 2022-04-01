from sqlalchemy import Column, String, Boolean

from . import Base, BaseMixin
class User(Base, BaseMixin):

    username = Column(String, index=True, unique=True)
    accountname = Column(String, index=True)
    password = Column(String)
    email = Column(String, index=True,)
    active = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    

    def __repr__(self):
        return "<User {}>".format(self.username)