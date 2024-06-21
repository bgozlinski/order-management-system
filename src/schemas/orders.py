from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class OrderSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    creation_date: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True)