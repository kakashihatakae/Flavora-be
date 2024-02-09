from enum import Enum
from database import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship


class OrderModes(Enum):
    DELIVERY = "DELIVERY"
    PICKUP = "PICKUP"


class Orders(Base):
    __tablename__ = "Orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(Integer, default=int(datetime.now().timestamp()))
    ordered_items = relationship("OrderedItems", backref="Orders")
    user_id = Column(Integer, ForeignKey("User.id"))
    menu_id = Column(Integer, ForeignKey("Menus.menu_id"))
    order_mode = Column(SQLAlchemyEnum(OrderModes), default=OrderModes.PICKUP)


# foreign key : https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
class OrderedItems(Base):
    __tablename__ = "OrderedItems"
    ordered_item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("Items.item_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("Orders.order_id"), nullable=False)
    count = Column(Integer, nullable=False)
