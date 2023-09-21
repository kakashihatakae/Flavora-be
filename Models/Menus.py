from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class Menus(Base):
    __tablename__ = "Menus"
    menu_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_owner_id = Column(Integer, ForeignKey("User.id"))
    title = Column(String(50), nullable=False)
    order_deadline = Column(DateTime, nullable=False)
    delivery_estimate = Column(DateTime, nullable=False)

    # orders from users that have this menu
    orders = relationship("Orders", backref="Menus")

    # items that are present in this menu
    items = relationship("MenuItems", backref="Menus")


class MenuItems(Base):
    __tablename__ = "MenuItems"
    menu_items_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("Menus.menu_id"))
    item_id = Column(Integer, ForeignKey("Items.item_id"))
