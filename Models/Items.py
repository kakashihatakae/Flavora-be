from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Items(Base):
    __tablename__ = "Items"
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String(200))
    price = Column(Integer)
    # users who have added these items, owners
    item_owner_id = Column(Integer, ForeignKey("User.id"))
    name = Column(String(100))

    # orders containing this particular item
    ordered_items = relationship("OrderedItems", backref="Items")

    # Menus that have this item
    menus = relationship("MenuItems", backref="Items")
