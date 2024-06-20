from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True