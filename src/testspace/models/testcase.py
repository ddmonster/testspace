from sqlalchemy import Column, String, Boolean,Text
from . import BaseMixin, Base
from .redbtype import StringList,JSONList,UUIDList, JsonText

class Testcase(Base, BaseMixin):
    name = Column(String,unique=True)
    description = Column(Text, default="")
    precondition = StringList()
    steps = JSONList()
    affect = StringList()
    component = StringList()
    suites = UUIDList()
    lables = StringList()
    deleted = Column(Boolean, default=False)

class TestSuite(Base, BaseMixin):
    name = Column(String)
    description = Column(Text)
    enums = JsonText()
    testplans = UUIDList()
    
class TestPlan(Base, BaseMixin):
    name = Column(String)
    description = Column(Text)

