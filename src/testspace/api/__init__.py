from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from testspace.crud.common import PageDescription,R_page,R_page_description,R_get_by_uuid

from testspace.db.session import get_db, Session

def set_page_enable_api(router:APIRouter, cls, ItemProps: BaseModel):
    """
    @router.get("/page/description", response_model=PageDescription )
    @router.get("/page/{index}", response_model=List[ItemProps])
    @router.get("/{uuid}", response_model=ItemProps)
    """
    @router.get("/page/description", response_model=PageDescription )
    async def  get_page_description(page_size:Optional[int]=None, session: Session = Depends(get_db)):
        with session.begin():
            if page_size:
                return R_page_description(session,cls,page_size)
            return R_page_description(session,cls)

    @router.get("/page/{index}", response_model=List[ItemProps])
    async def get_page(index:int, page_size:Optional[int] = None, session: Session = Depends(get_db)):
        with session.begin():
            if page_size:
                return R_page(session ,cls,index,page_size)
            return R_page(session ,cls,index)

    @router.get("/item/{uuid}", response_model=ItemProps)
    async def get_Item_by_uuid(uuid: UUID,session: Session = Depends(get_db)):
        with session.begin() as s :
            return R_get_by_uuid(session ,cls,uuid)