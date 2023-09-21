from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Orders(Base):
    __tablename__ = "Orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    ordered_items = relationship("OrderedItems", backref="Orders")
    user_id = Column(Integer, ForeignKey("User.id"))
    menu_id = Column(Integer, ForeignKey("Menus.menu_id"))


# foreign key : https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html
class OrderedItems(Base):
    __tablename__ = "OrderedItems"
    ordered_item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("Items.item_id"))
    order_id = Column(Integer, ForeignKey("Orders.order_id"))
