from typing import List,Optional,Mapping
from sqlalchemy import VARCHAR
from sqlalchemy.dialects.postgresql import UUID as PGUUID,JSON
from sqlmodel import Relationship, SQLModel,Field,Column
from uuid import uuid4,UUID

class UserGroupLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True
    )
    group_id: Optional[int] = Field(
        default=None, foreign_key="usergroup.id", primary_key=True
    )
    
class UserGroup(SQLModel,table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: UUID = Field(...,sa_column=Column(PGUUID(as_uuid=True),default=uuid4,index=True))
    name:str
    property: Mapping[str,str] = Field({},sa_column=Column(JSON(astext_type=True)))
    users: List["User"] = Relationship(back_populates="groups",link_model=UserGroupLink)
    
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    uuid: UUID = Field(...,sa_column=Column(PGUUID(as_uuid=True),default=uuid4,index=True))
    username: str = Field(...,sa_column=Column(VARCHAR,unique=True,index=True))
    password: str 
    email : Optional[str]
    phone : Optional[str]
    active: Optional[bool] = Field(sa_column_kwargs={"default":True})
    admin: Optional[bool] = Field(sa_column_kwargs={"default":False})
    avatar: Optional[str] = Field(sa_column=Column(VARCHAR))
    property: Mapping[str,str] = Field({},sa_column=Column(JSON(astext_type=True)))
    groups: List[UserGroup] = Relationship(back_populates="users",link_model=UserGroupLink)
    
