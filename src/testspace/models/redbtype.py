from email.policy import default
from typing import Union, List
from pydantic import Json
from sqlalchemy import Column,String
from sqlalchemy.dialects.postgresql import UUID,ARRAY, JSON



def StringList(*args,**kwargs) -> Union[Column,List[str]]:
    return Column(ARRAY(String,as_tuple=True),*args, **kwargs)

def JSONList(*args,**kwargs) -> Union[Column,List[Json]]:
    return Column(ARRAY(JSON(astext_type=True),as_tuple=True),*args, **kwargs)
    
def UUIDList(*args,**kwargs) -> Union[Column, List[UUID]]:
    return Column(ARRAY(UUID(as_uuid=True),as_tuple=True),*args, **kwargs)

def JsonText(*args, **kwargs) ->Union[Column,Json]:
    return Column(JSON(astext_type=True),*args,**kwargs)

