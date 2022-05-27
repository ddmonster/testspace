
from enum import Enum
from optparse import Option
from uuid import UUID
from sqlalchemy import desc, func
from sqlalchemy.orm import Session, Query
from typing import Any, List, Literal, Optional, Type, TypeVar, Union
import math
from pydantic import BaseModel
from testspace.db.base_class import Base
DBModels = Type[Base]


class PageDescription(BaseModel):
    total_items: int
    page_size: int
    max_index: int


class FilterType(Enum):
    EQUAL = "equal"
    CONTAINS = "contains"
    GT = "gt"

class FilterParam(BaseModel):
    type: FilterType
    prop: str
    value: Union[str,List[str]] 

class OrderParam(BaseModel):
    prop:str
    order: Literal["desc", "asc"]
    
class QueryParam(BaseModel):
    cur_page: int
    page_size: int
    filters: List[FilterParam]
    order: Optional[OrderParam]


class QueryResult(QueryParam):
    data: List

    
def filter_query(q: Query, params: List[FilterParam], models):
    query = q
    for filter in params:
        prop = getattr(models, filter.prop, None)
        if prop is None:
            raise Exception(f"{models} have no prop {filter.prop}, wrong filter {filter}")
        if filter.type == FilterType.EQUAL:
            query = query.filter_by(**{filter.prop: filter.value})
        elif filter.type == FilterType.CONTAINS:
            if type(filter.value) is str or type(filter.value) is list:
                query = query.filter(
                    prop.contains(filter.value))
            else:
                raise Exception("unsuported filter value ")
                
        else:
            raise Exception(f"no such type {filter.type}")
    return query


def R_get_pages(s: Session, cls: DBModels, query: QueryParam):
    result = QueryResult(**query.dict(),data=[])
    query_stmt = filter_query(s.query(cls), query.filters, cls)
    if query.order:
        order_prop = getattr(cls, query.order.prop)
        query_stmt = query_stmt.order_by(desc(order_prop) if query.order.order == "desc" else order_prop)
    row_count = query_stmt.count()
    _pages = math.ceil(row_count/query.page_size) - 1
    if _pages == -1:
        result.data = []
        return result
    if query.cur_page > _pages:
        raise Exception(f"out of page size max:{_pages}")
    result.data = query_stmt.offset(
        query.cur_page*query.page_size).limit(query.page_size).all()
    return result


def R_page(s: Session, cls: DBModels, page: int, page_size: int = 100) -> List[DBModels]:
    r'''
    get specific page from table

    Args:
        page:       start from 0 if extend the edge will raise Exception("out of page size")
        page_size:  defult 100 use to count the total pages all_rows/page_size
    '''
    if page_size == -1:
        return s.query(cls).all()
    row_count = s.query(cls).count()
    _pages = math.ceil(row_count/page_size) - 1
    if _pages == -1:
        return []
    if page > _pages:
        raise Exception(f"out of page size max:{_pages}")
    return s.query(cls).offset(page*page_size).limit(page_size).all()


def R_page_description(s: Session, cls: DBModels,  page_size=100) -> PageDescription:
        row_count = s.query(cls).count()
        if page_size == -1:
            return PageDescription(total_items=row_count, page_size=page_size, max_index=0)
        return PageDescription(total_items=row_count, page_size=page_size, max_index=math.ceil(row_count/page_size) - 1)


def R_get_by_uuid(s: Session, cls: DBModels, uuid: UUID) -> Union[None, DBModels]:
    rs = s.query(cls).filter_by(uuid=uuid).first()
    return rs
