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
    labels = StringList()
    deleted = Column(Boolean, default=False)
    enums = JsonText()
class TestSuite(Base, BaseMixin):
    name = Column(String)
    description = Column(Text)
    enums = JsonText()
    labels = StringList()
    testplans = UUIDList()
    
class TestPlan(Base, BaseMixin):
    name = Column(String)
    description = Column(Text)
    labels = StringList()
    enums = JsonText()

