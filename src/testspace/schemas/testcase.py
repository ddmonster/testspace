from pydoc import describe
from typing import Optional,List
from pydantic import BaseModel
from uuid import UUID
from . import CommonProps
class UseORM(BaseModel):
    class Config:
        orm_mode = True


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
    lables : List[str]
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
    lables : Optional[List[str]]
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
    lables : Optional[List[str]]

class TestSuitProps(UseORM, CommonProps):
    name:str
    description: str
    enums: dict
    testplans:List[UUID]
class TestSuitCreate(BaseModel):
    name:str
    description: str
    enums: dict
    create_by: Optional[UUID]
    testplans:List[UUID]
class TestSuitUpdate(BaseModel):
    uuid:Optional[UUID]
    update_by: Optional[UUID]
    name:Optional[str]
    description: Optional[str]
    enums: Optional[dict]
    testplans:Optional[List[UUID]]
    
class TestPlanProps(UseORM,CommonProps):
    name: str
    description:str

class TestPlanCreate(BaseModel):
    name: str
    description:str
    create_by:UUID
    
class TestPlanUpdate(BaseModel):
    name: Optional[str]
    description:Optional[str]
    update_by:Optional[UUID]
    





