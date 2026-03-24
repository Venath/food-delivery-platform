# restaurant-service/models.py
from pydantic import BaseModel
from typing import Optional

class Restaurant(BaseModel):
    id: int
    name: str
    address: str
    phone: str
    cuisine_type: str
    rating: float
    is_open: bool

class RestaurantCreate(BaseModel):
    name: str
    address: str
    phone: str
    cuisine_type: str
    rating: float
    is_open: bool = True

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    cuisine_type: Optional[str] = None
    rating: Optional[float] = None
    is_open: Optional[bool] = None
