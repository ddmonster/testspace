from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from . import Base, TableCRUD
from testspace.utils.gen import uuid_v4, curtime


class Table(Base,TableCRUD):
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False,default=uuid_v4)
    name = Column(String, unique=True, nullable=False)
    table_scheme = Column(Text,nullable=False)
    created_at = Column(DateTime, default=curtime)
    updated_at = Column(DateTime, default=curtime, onupdate=curtime)



