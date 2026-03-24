# menu-service/models.py
from pydantic import BaseModel
from typing import Optional

class MenuItem(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str
    price: float
    category: str
    is_available: bool

class MenuItemCreate(BaseModel):
    restaurant_id: int
    name: str
    description: str
    price: float
    category: str
    is_available: bool = True

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
