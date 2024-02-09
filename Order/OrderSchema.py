from typing import List
from pydantic import BaseModel, PositiveFloat
from Models.Orders import OrderModes


class OrderedItemSchema(BaseModel):
    item_id: int
    count: int


class OrderSchema(BaseModel):
    menu_id: int
    items: List[OrderedItemSchema]
    order_mode: OrderModes
