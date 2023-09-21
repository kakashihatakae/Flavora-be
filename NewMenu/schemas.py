from typing import List
from datetime import datetime
from pydantic import BaseModel, PositiveFloat


class NewItem(BaseModel):
    price: PositiveFloat
    name: str
    image: str  # change


class NewMenu(BaseModel):
    order_deadline: datetime
    delivery_estimate: datetime
    item_ids: List[int]
    title: str
