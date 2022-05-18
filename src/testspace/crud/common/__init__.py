
from enum import Enum
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import Session, Query
from typing import Any, List, TypeVar, Union
import math
from pydantic import BaseModel
from testspace.db.base_class import Base
DBModels = Base


class PageDescription(BaseModel):
    total_items: int
    page_size: int
    max_index: int


class FilterType(Enum):
    EQUAL = "equal"
    CONTAINS = "contains"


class FilterParam(BaseModel):
    type: FilterType
    prop: str
    value: str


class QueryParam(BaseModel):
    cur_page: int
    page_size: int
    filter: List[FilterParam]


class QueryResult(QueryParam):
    data: List

    
def filter_query(q: Query, params: List[FilterParam], tbj):
    query = q
    for filter in params:
        if filter.type == FilterType.EQUAL:
            query = query.filter_by(**{filter.prop: filter.value})
        elif filter.type == FilterType.CONTAINS:
            query = query.filter(
                getattr(tbj, filter.prop).contains(filter.value))
    return query


def R_get_pages(s: Session, cls: DBModels, query: QueryParam):
    result = QueryResult(**query.dict())
    query_stmt = filter_query(s.query(cls), query.filter, cls)
    row_count = query_stmt.count()
    _pages = math.ceil(row_count/query.page_size) - 1
    if _pages == -1:
        result.data = []
        return result
    if query.cur_page > _pages:
        raise Exception(f"out of page size max:{_pages}")
    result.data = s.query(cls).offset(
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
    with s.begin():
        row_count = s.query(cls).count()
        if page_size == -1:
            return PageDescription(total_items=row_count, page_size=page_size, max_index=0)
        return PageDescription(total_items=row_count, page_size=page_size, max_index=math.ceil(row_count/page_size) - 1)


def R_get_by_uuid(s: Session, cls: DBModels, uuid: UUID) -> Union[None, DBModels]:
    rs = s.query(cls).filter_by(uuid=uuid).first()
    return rs
