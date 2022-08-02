
from typing import List, Literal, Optional
from pydantic import UUID4 as UUID
from pydantic import Extra
from sqlalchemy.dialects.postgresql import UUID as PGUUID,JSON,ARRAY
from sqlalchemy.orm import backref
from typing import Mapping
from sqlmodel import VARCHAR,  Relationship, SQLModel, Field,Column,Text,BOOLEAN
from uuid import uuid4
class TestItem(SQLModel, table=True, extra=Extra.allow):
    id: int = Field(default=None, primary_key=True)
    uuid: Optional[UUID] = Field(...,sa_column=Column(PGUUID(as_uuid=True),default=uuid4,index=True,unique=True))
    name: str = Field(...,sa_column=Column(VARCHAR,unique=True))
    type: Literal["TestPlan","TestCase","TestSuite","Free"] = Field(...,sa_column=Column(VARCHAR,default="Free"))
    description: str = Field(...,sa_column=Column(Text))
    property: Mapping[str,str] = Field({},sa_column=Column(JSON(astext_type=True)))
    labels: List[str] = Field([],regex="[a-z_]*",sa_column=Column(ARRAY(VARCHAR,as_tuple=True)))
    deleted: bool =  Field(False,sa_column=Column(BOOLEAN,default=False))
    parent_id: Optional[int] = Field(default=None, foreign_key='testitem.id',nullable=True)
    children: List["TestItem"] = Relationship(
    sa_relationship_kwargs=dict(
      cascade="all",
      backref=backref("parent", remote_side="TestItem.id"),
    )  
  )


if __name__ == "__main__":
    pass