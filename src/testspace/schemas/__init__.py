from typing import Optional,TypeVar, Union
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

T = TypeVar("T")
AdditionalProp = Optional[T]
"""equals to Optional[] to info this property is not original database modal """
class CommonProps(BaseModel):
    """
    uuid:UUID
    created_at:datetime
    updated_at: datetime
    update_by:UUID
    create_by:UUID
    """
    uuid:UUID
    created_at:datetime
    updated_at: datetime
    update_by:Optional[UUID]
    create_by:Optional[UUID]
    

    
