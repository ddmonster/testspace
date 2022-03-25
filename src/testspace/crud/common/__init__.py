
from sqlalchemy.orm import Session
from typing import List, TypeVar, Union
import math
from pydantic import BaseModel

DBModels = TypeVar("DBModels")

class PageDescription(BaseModel):
    total_items:int
    page_size: int
    max_index:int

def R_page(s: Session, cls:DBModels, page:int, page_size=100) -> List[DBModels]:
    r'''
    get specific page from table

    Args:
        page:       start from 0 if extend the edge will raise Exception("out of page size")
        page_size:  defult 100 use to count the total pages all_rows/page_size
    '''
    row_count = s.query(cls).count()
    _pages = math.ceil(row_count/page_size) - 1
    if _pages == -1:
        return []
    if page > _pages:
        raise Exception(f"out of page size max:{_pages}")
    return s.query(cls).offset(page*page_size).limit(page_size).all()

def R_page_description(s: Session,cls:DBModels,  page_size=100)-> PageDescription:
    row_count =  s.query(cls).count()
    return PageDescription(total_items= row_count,page_size = page_size,max_index=math.ceil(row_count/page_size) - 1)

def R_get_by_uuid(s: Session, cls:DBModels, uuid) -> Union[None, DBModels]:
    rs = s.query(cls).filter_by(uuid=uuid).first()
    return rs
            