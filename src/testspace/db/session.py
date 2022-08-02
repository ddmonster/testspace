
from functools import cache
from testspace.log import logger
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.engine.base import Engine

# issue fix for sqlmodel
# https://github.com/tiangolo/sqlmodel/issues/189#issuecomment-1065790432
from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

__all__ = [
    "get_engine",
    "engine"
]
engine:Engine 

@cache
def get_engine(SQLALCHEMY_DATABASE_URL):
    global engine
    if not  database_exists(SQLALCHEMY_DATABASE_URL):
        create_database(SQLALCHEMY_DATABASE_URL)
    engine = create_engine(SQLALCHEMY_DATABASE_URL,query_cache_size=1200)
    try:
        engine.execute("SELECT 1")
    except Exception as e :
        logger.error(f"connect to db {SQLALCHEMY_DATABASE_URL} failed {repr(e)}")
        raise e
    logger.info(f"connect to db {SQLALCHEMY_DATABASE_URL} success ")
        
    return engine
