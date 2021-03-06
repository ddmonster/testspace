
from contextvars import ContextVar
from typing import Any, Optional, TypeVar, Generic
__all__ = ["ContextWarpper"]
T = TypeVar("T")

class ContextWarpper(Generic[T]):
    def __init__(self,name:str,value:Optional[T]) -> None:
        
        self.__var = ContextVar(name,default=value)
        
    def __getattr__(self,__name):
        return getattr(self.__var.get(), __name)
    def get(self):
        return self.__var.get()
    def set(self,value:T):
        self.__var.set(value)


