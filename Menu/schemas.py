from typing import List
from pydantic import BaseModel, PositiveFloat


class ItemSchema(BaseModel):
    price: PositiveFloat
    name: str
    image: str  # change


class MenuSchema(BaseModel):
    order_deadline: int
    delivery_estimate: int
    item_ids: List[int]
    title: str
