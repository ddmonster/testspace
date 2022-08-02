
from pydantic import BaseModel
from  sqlalchemy.engine.base import Engine
from sqlmodel import Session,select,SQLModel
from typing import Type

# https://docs.sqlalchemy.org/en/14/core/tutorial.html#version-check
# def filter(Model:Type[SQLModel],engine:Engine,compare:BaseModel):
#     compare.
#     with Session(engine) as s:
#         s.exec(select(Model).where(Model.name == "1"))