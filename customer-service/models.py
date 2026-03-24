# customer-service/models.py
from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    city: str
    is_active: bool

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    city: str
    is_active: bool = True

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None
