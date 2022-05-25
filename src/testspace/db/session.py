from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from testspace.config import tomlconfig
from testspace.log import logger

__all__ = [
    'session',
    'openSession',
    "get_db"
]

SQLALCHEMY_DATABASE_URL  = tomlconfig.database.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
logger.info(f"database set up {tomlconfig.database.SQLALCHEMY_DATABASE_URL}")
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

# _async_session = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )
# Async_session =  async_scoped_session(_async_session, scopefunc=current_task)
SessionLocal = scoped_session(sessionmaker(autocommit=False, bind=engine))

session:Session =SessionLocal()


@contextmanager
def openSession():
    '''for context use'''
    db:Session = session
    try:
        yield db
    finally:
        db.close()

def get_db():
    '''for fastapi dependence only'''
    db:Session = session
    try:
        yield db
    finally:
        db.close()