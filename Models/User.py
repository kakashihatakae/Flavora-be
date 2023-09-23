from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(10), nullable=False)
    name = Column(String(100))
    email = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

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
