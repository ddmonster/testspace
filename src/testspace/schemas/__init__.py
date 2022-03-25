from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


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