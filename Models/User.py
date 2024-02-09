from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(10), nullable=False)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    image = Column(String(200))
    addressLine1 = Column(String(100))
    addressLine2 = Column(String(100))
    city = Column(String(50))
    state = Column(String(50))
    zipCode = Column(String(20))
    country = Column(String(50))
    delivery = Column(Boolean, default=False)
    pickup = Column(Boolean, default=False)

    # items ordered by a user
    orders = relationship("Orders", backref="User")

    # items added by a specific chef/owner
    items = relationship("Items", backref="User")

    # Menus added by a specific chef/owner
    menus = relationship("Menus", backref="User")


class Roles:
    USER = "user"
    VENDOR = "vendor"
    DRIVER = "driver"
