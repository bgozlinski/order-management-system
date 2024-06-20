from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderSchema(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    creation_date: Optional[datetime]
    status: str

    class Config:
        orm_mode = True