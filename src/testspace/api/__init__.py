from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from testspace.db.base_class import Base

def set_common_api(router:APIRouter, model:Base, PageDescription:BaseModel, ItemProps: BaseModel, ItemCreate: BaseModel, ItemUpdate: BaseModel):
    @router.get("/page/description", response_model=PageDescription)
    def get_page_description(page_size:Optional[int]=None):
        if page_size:
            return model.page_description(page_size=page_size)
        return model.page_description()

    @router.get("/page/{index}", response_model=List[ItemProps])
    def get_page(index:int, page_size:Optional[int] = None):
        if page_size:
            return model.page(index,page_size=page_size)
        return model.page(index)

    @router.get("/{uuid}", response_model=ItemProps)
    def get_Item_by_uuid(uuid: UUID):
        return model.select_by_uuid(uuid)

    @router.post("/",status_code=201, response_model=ItemProps)
    def create_item(item: ItemCreate):
        _item = model(**item.dict())
        return model.add(_item)

    @router.put("/{uuid}", response_model=ItemProps)
    def update_Item(uuid:UUID,  item: ItemUpdate):
        return model.update_item(uuid, **item.dict())