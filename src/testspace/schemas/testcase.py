from typing import Optional
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
    precondition:list[str]
    steps:list[Steps]
    affect : list[str]
    component : list[str]
    suites: list[UUID]
    lables : list[str]
    deleted: bool

class TestcaseUpdate(BaseModel):
    uuid: UUID
    name:str
    update_by:Optional[UUID]
    precondition:Optional[list[str]]
    steps:Optional[list[Steps]]
    affect : Optional[list[str]]
    component : Optional[list[str]]
    suites: Optional[list[UUID]]
    lables : Optional[list[str]]
    deleted: Optional[bool]

class TestcaseCreate(BaseModel):
    name:str
    create_by:Optional[UUID]
    update_by:Optional[UUID]
    precondition:Optional[list[str]]
    steps:Optional[list[Steps]]
    affect : Optional[list[str]]
    component : Optional[list[str]]
    suites: Optional[list[UUID]]
    lables : Optional[list[str]]

class TestSuitProps(UseORM, CommonProps):
    name:str
    description: str
    enums: dict

class TestSuitCreate(BaseModel):
    name:str
    description: str
    enums: dict
    create_by: Optional[UUID]

class TestSuitUpdate(BaseModel):
    uuid:UUID
    update_by: Optional[UUID]
    name:Optional[str]
    description: Optional[str]
    enums: Optional[dict]









