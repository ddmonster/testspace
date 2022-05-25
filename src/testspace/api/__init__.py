from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Any, Optional, List
from testspace.crud.common import PageDescription,R_page,R_page_description,R_get_by_uuid, R_get_pages, QueryResult, QueryParam

from testspace.db.Session import session

def set_page_enable_api(router:APIRouter, cls, ItemProps: Any):
    """
    @router.get("/page/description", response_model=PageDescription )
    @router.get("/page/{index}", response_model=List[ItemProps])

    """
    @router.get("/page/description", response_model=PageDescription )
    async def  get_page_description(page_size:Optional[int]=None):
            if page_size:
                return R_page_description(session,cls,page_size)
            return R_page_description(session,cls)

    @router.get("/page/{index}", response_model=List[ItemProps])
    async def get_page(index:int, page_size:Optional[int] = None, ):
            if page_size:
                return R_page(session ,cls,index,page_size)
            return R_page(session ,cls,index)
    @router.post("/pages/", response_model= QueryResult)
    async def get_pages(query:QueryParam):
            return R_get_pages(session,cls,query)
    # @router.get("/item/{uuid}", response_model=ItemProps)
    # async def get_Item_by_uuid(uuid: UUID,session: Session = Depends(get_db)):
    #     with session.begin() as s :
    #         return R_get_by_uuid(session ,cls,uuid)