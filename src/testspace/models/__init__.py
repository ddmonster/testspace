from typing import Dict, Optional
from sqlalchemy import Column, DateTime, Integer, Table
from testspace.db.base_class import Base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
# https://docs.sqlalchemy.org/en/14/dialects/postgresql.html#dialect-postgresql
import datetime
def curtime() -> datetime.datetime:
    return datetime.datetime.now()
def uuid_v4():
    import uuid
    return uuid.uuid4()

__all__ = [
    "BaseMixin",
    "Base"
]
class BaseMixin(object):
    '''
    Note: make class name as table name
    __name__: str
    __db_prefix__: Optional[str] = None
    __table__:Table
    __table_args__ = {"extend_existing":True}

    internal columns:
    
        id = Column(Integer, primary_key=True)
        
        uuid = Column(UUID, unique=True, nullable=False, default=uuid_v4)
        
        created_at = Column(DateTime, default=curtime)
        
        updated_at = Column(DateTime, default=curtime, onupdate=curtime)
        
        update_by = Column(UUID)
        
        create_by = Column(UUID)

    '''
    __name__: str
    __db_prefix__: Optional[str] = None
    __table__:Table
    __table_args__ = {"extend_existing":True}

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid_v4)
    created_at = Column(DateTime, default=curtime)
    updated_at = Column(DateTime, default=curtime, onupdate=curtime)
    update_by = Column(UUID(as_uuid=True))
    create_by = Column(UUID(as_uuid=True))
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        if getattr(cls, '__db_prefix__', None):
            return f"{cls.__db_prefix__}_{cls.__name__}".lower()
        return cls.__name__.lower()





        