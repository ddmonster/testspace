from sqlalchemy import Column, String, Boolean,Text
from sqlalchemy.dialects.postgresql import UUID,ARRAY, JSON, array
from . import BaseMixin, Base

class Testcase(Base, BaseMixin):
    name = Column(String,unique=True)
    description = Column(Text, default="")
    precondition = Column(ARRAY(String,as_tuple=True))
    steps = Column(ARRAY(JSON(astext_type=True),as_tuple=True))
    affect = Column(ARRAY(String,as_tuple=True))
    component = Column(ARRAY(String, as_tuple=True))
    suites = Column(ARRAY(UUID(as_uuid=True),as_tuple=True))
    lables = Column(ARRAY(String,as_tuple=True))
    deleted = Column(Boolean, default=False)

class TestSuite(Base, BaseMixin):
    name = Column(String)
    description = Column(Text)
    enums = Column(JSON(astext_type=True))

