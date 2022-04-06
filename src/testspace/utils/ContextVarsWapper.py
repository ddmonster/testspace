
from contextvars import ContextVar
from typing import Any



class ContextWarpper(object):
    def __init__(self,name:str,value:Any) -> None:
        
        self.__var = ContextVar(name,default=value)
        
    def __getattr__(self,__name):
        return getattr(self.__var.get(), __name)
    
    def set(self,value):
        self.__var.set(value)
        
    def __str__(self) -> str:
        return self.__var.get().__str__()


