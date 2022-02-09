from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from testspace.config import tomlconfig


SQLALCHEMY_DATABASE_URL  = tomlconfig["database"]["SQLALCHEMY_DATABASE_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
