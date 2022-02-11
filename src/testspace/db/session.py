from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, Query

from testspace.config import tomlconfig


SQLALCHEMY_DATABASE_URL  = tomlconfig["database"]["SQLALCHEMY_DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_session():
    '''get session in context, after exit will close session'''
    session:Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
