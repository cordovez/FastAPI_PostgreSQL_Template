from pydantic import BaseModel
from typing import Optional


class ItemSchema(BaseModel):
    name: str
    description: str
    belongs_to_id: Optional[int] = None
