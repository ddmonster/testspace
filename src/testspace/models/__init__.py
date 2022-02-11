from typing import Dict
from testspace.db.base_class import Base
from testspace.db.session import get_session, Query
import math
from uuid import UUID
class TableCRUD:
    @classmethod
    def page(cls, page:int, page_size=100):
        r'''
        get specific page from table

        Args:
            page:       start from 0 if extend the edge will raise Exception("out of page size")
            page_size:  defult 100 use to count the total pages all_rows/page_size
        '''
        _pages = math.ceil(cls.row_count()/page_size) - 1
        if page > _pages:
            raise Exception("out of page size")
        with get_session() as session:
            return session.query(cls).offset(page*page_size).limit(page_size).all()

    @classmethod
    def page_description(cls,  page_size=100):
        rows = cls.row_count()
        return {
            "total_items": rows,
            "max_index": math.ceil(rows/page_size) - 1,
            "page_size": page_size
        }

    @classmethod
    def row_count(cls):
        with get_session() as session:
            return session.query(cls).count()

    @classmethod
    def select_by_uuid(cls, uuid:UUID):
        with get_session() as session:
            item = cls._get_item_by_uuid(session, uuid).first()
            if not item:
                raise Exception(f"no such item {uuid} in {cls.__name__}")
            return item

    @classmethod
    def update_item(cls, uuid, **kw):
        with get_session() as session:
            query = session.query(cls).filter_by(uuid=uuid.__str__())
            item = query.first()
            if not item:
                raise Exception(f"no such item {uuid} in {cls.__name__}")

            query.update(kw)
            session.commit()
            session.refresh(item)
            return item

    @classmethod
    def add(cls, obj):
        with get_session() as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj

    @classmethod
    def _get_item_by_uuid(cls,session,uuid) -> Query:
        return session.query(cls).filter_by(uuid=uuid.__str__())
        