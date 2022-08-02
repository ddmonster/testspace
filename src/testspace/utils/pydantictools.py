from inspect import isclass
from typing import TYPE_CHECKING,Union,Optional
from pydantic import BaseModel
import typing
import copy
from functools import cache
# class Partial:
#     def __class_getitem__(cls,item):
#         field = {}
#         for i in item.__annotations__.keys():
#             if item.__module__ == typing:
#                 if item.__annotations__[i].__origin__ == Union and item.__annotations__[i].__args__[1] == None:
#                     continue
#             field[i] = (Optional[item.__annotations__[i]],None)
#         return create_model("t",__config__=item.__dict__["__config__"],**field)

@cache
def partial_func_cached(name,cls,exclude_params=[]):
        annotations = cls.__annotations__.copy()
        fields =  copy.deepcopy(cls.__fields__)
        
        for i in annotations.keys():
            if i in exclude_params:
                continue
            if cls.__module__ == typing:
                if annotations[i].__origin__ == Union and annotations[i].__args__[1] == None:
                    continue 
            annotations[i] = Optional[annotations[i]] # type: ignore
        NewType = type(name,(BaseModel,),{
            "__annotations__":annotations,
            "__fields__":fields
        })  
        for i in NewType.__fields__.keys():
            NewType.__fields__[i].required = False
        return NewType
    
@cache
def omit_func_cached(name,omit_cls,*omit_params):
        annotations = omit_cls.__annotations__.copy()
        fields = omit_cls.__fields__.copy()
        for i in omit_params:
            del annotations[i]
            del fields[i]
        NewType = type(name,(BaseModel,),{
            "__annotations__":annotations,
            "__fields__":fields,
            
        })  
        return NewType
@cache
def pick_func_cached(name,pick_cls,*pick_params):
        annotations = pick_cls.__annotations__.copy()
        fields = pick_cls.__fields__.copy()
        
        for i in set(annotations.keys()) - set(pick_params):
            del annotations[i]
            del fields[i]
        _pydantic_type = type(name,(BaseModel,),{
            "__annotations__":annotations,
            "__fields__":fields,
            
        })  
        return _pydantic_type
class Partial(BaseModel):
    
    def __class_getitem__(cls,items):
        first_param, *params = items
        exclude = []
        if isclass(first_param):
            if all(params):
                exclude = params
                return partial_func_cached("_",first_param,*exclude)
        return partial_func_cached(first_param,params[0])

class Pick(BaseModel):
    def __class_getitem__(cls,items):
        """Pick[Cls, "name","property"]"""
        first_param, *params = items
        if isclass(first_param):
            params.sort()
            return pick_func_cached("_", first_param,*params)
        pick_cls, *pick_params = params
        pick_params.sort()
        return pick_func_cached(first_param, pick_cls,*pick_params)
    
class Omit(BaseModel):
    """Omit[Cls, "name","property"]
    
        class User(BaseModel):
            id:int = Feild(...,primary_key=True)
            name:str
            password:str
            avator:str
        UserUpdate = Omit[User,"id"]
    """
        
    def __class_getitem__(cls,items):
        first_param, *params = items
        if isclass(first_param):
            params.sort()
            return omit_func_cached("_", first_param,*params)
        omit_cls,*omit_params = params
        return omit_func_cached(first_param, omit_cls,*omit_params)
        
        

# class Omit:
#     def __class_getitem__(cls,item):
#         org, *om = item
#         field = {}
#         for i in org.__annotations__.keys():
#             if i in om:
#                 continue
#             field[i] = org.__annotations__[i]
#         return create_model("t",__config__=org.__dict__["__config__"],**field)