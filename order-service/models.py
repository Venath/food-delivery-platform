# order-service/models.py
from pydantic import BaseModel
from typing import Optional, List

class OrderItem(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    unit_price: float
    subtotal: float

class Order(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    items: List[OrderItem]
    total_amount: float
    status: str  # pending, confirmed, preparing, out_for_delivery, delivered, cancelled
    delivery_address: str
    notes: Optional[str] = None

class OrderCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    items: List[OrderItem]
    total_amount: float
    delivery_address: str
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
