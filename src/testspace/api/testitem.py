
from testspace.models.testitem import TestItem
from fastapi import APIRouter,Depends
from testspace.utils.pydantictools import Omit,Partial
from testspace.components.auth import oauth2_scheme
from sqlmodel import Session,select       
from uuid import UUID                               
from testspace.db.session import engine
from typing import List
router = APIRouter(tags=["testitem management"],dependencies=[Depends(oauth2_scheme)])
TestItemAdd = Omit["TestItemAdd",TestItem,"uuid","id","parent_id"]
TestItemUpdate = Partial["TestItemUpdate",TestItemAdd]



@router.post("/",response_model=TestItem)
async def add(item:TestItemAdd):
    with Session(engine) as s:
        _item = TestItem(**item.dict(exclude_unset=True))
        s.add(_item)
        s.commit()
        s.refresh(_item)
        return _item
# @router.get("/",response_model=List[TestItem])
# async def get():
    
@router.patch("/{id}",response_model=TestItem)
async def update(item:TestItemUpdate,id:UUID):
    with Session(engine) as s:
        new_item_prop = item.dict(exclude_unset=True)
        org_item = s.exec(select(TestItem).where(TestItem.uuid==id).where()).one()
        for k,v in new_item_prop.items():
            setattr(org_item,k,v)
        s.add(org_item)
        s.commit()
        s.refresh(org_item)
        return org_item
    
@router.get("/{id}",response_model=TestItem)
async def get_item(id:UUID):
    with Session(engine) as s:
        return s.exec(select(TestItem).where(TestItem.uuid == id)).one()
    
    
@router.get("/{id}/children",response_model=List[TestItem])
async def children(id:UUID):
    with Session(engine) as s:
        org_item = s.exec(select(TestItem).where(TestItem.uuid==id)).one()
        return org_item.children

