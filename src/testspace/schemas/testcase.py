
from typing import Optional,List
from pydantic import BaseModel
from uuid import UUID
from . import AdditionalProp, CommonProps
class UseORM(BaseModel):
    class Config:
        orm_mode = True
class UseArbitrary(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class Steps(UseORM):
    type:str
    action:str

class TestcaseProps(UseORM,CommonProps):
    name:str
    precondition:List[str]
    steps:List[Steps]
    affect : List[str]
    component : List[str]
    suites: List[UUID]
    labels : List[str]
    deleted: bool

class TestcaseUpdate(BaseModel):
    uuid: Optional[UUID]
    name:Optional[str]
    update_by:Optional[UUID]
    precondition:Optional[List[str]]
    steps:Optional[List[Steps]]
    affect : Optional[List[str]]
    component : Optional[List[str]]
    suites: Optional[List[UUID]]
    labels : Optional[List[str]]
    deleted: Optional[bool]

class TestcaseCreate(BaseModel):
    name:str
    create_by:Optional[UUID]
    update_by:Optional[UUID]
    precondition:Optional[List[str]]
    steps:Optional[List[Steps]]
    affect : Optional[List[str]]
    component : Optional[List[str]]
    suites: Optional[List[UUID]]
    labels : Optional[List[str]]

class TestSuitProps(UseORM, CommonProps):
    name:str
    description: str
    enums: dict
    testplans:List[UUID]
    labels : List[str]
    
class TestSuitCreate(BaseModel):
    name:str
    description: Optional[str]
    enums: Optional[dict]
    create_by: Optional[UUID]
    testplans:List[UUID]
    labels : Optional[List[str]]
    
class TestSuitUpdate(UseArbitrary,BaseModel):
    uuid:Optional[UUID]
    update_by: Optional[UUID]
    name:Optional[str]
    description: Optional[str]
    enums: Optional[dict]
    testplans:Optional[List[UUID]]
    labels : Optional[List[str]]
    testcases: AdditionalProp[List[TestcaseProps]]
class TestPlanProps(UseArbitrary,UseORM,CommonProps):
    name: str
    description:str
    enums:dict
    labels: List[str]
    testsuits:AdditionalProp[List[TestSuitProps]]
class TestPlanCreate(BaseModel):
    name: str
    description:Optional[str]
    create_by:Optional[UUID]
    enums: Optional[dict]
    labels: Optional[List[str]]
class TestPlanUpdate(BaseModel):
    name: Optional[str]
    description:Optional[str]
    update_by:Optional[UUID]
    enums: Optional[dict]
    labels : Optional[List[str]]
    





