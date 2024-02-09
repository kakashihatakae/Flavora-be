from typing import List, Optional, Union
from pydantic import BaseModel


class UserInformation(BaseModel):
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    city: Optional[str]
    name: Optional[str]
    state: Optional[str]
    zipCode: Optional[str]
    country: Optional[str]
    pickup: bool
    delivery: bool


class ImageUrl(BaseModel):
    url: str
