from email.policy import default
from sqlalchemy import Column, String, Boolean,Text
from . import BaseMixin, Base
from .redbtype import StringList,JSONList,UUIDList, JsonText

class Testcase(Base, BaseMixin):
    name = Column(String,unique=True)
    description = Column(Text, default="")
    precondition = StringList(default=[])
    steps = JSONList(default=[])
    affect = StringList(default=[])
    component = StringList(default=[])
    suites = UUIDList(default=[])
    labels = StringList(default=[])
    deleted = Column(Boolean, default=False)
    enums = JsonText(default={})
class TestSuite(Base, BaseMixin):
    name = Column(String)
    description = Column(Text,default='')
    enums = JsonText(default={})
    labels = StringList(default=[])
    testplans = UUIDList(default=[])
    
class TestPlan(Base, BaseMixin):
    name = Column(String)
    description = Column(Text,default='')
    labels = StringList(default=[])
    enums = JsonText(default={})

