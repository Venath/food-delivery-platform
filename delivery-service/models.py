# delivery-service/models.py
from pydantic import BaseModel
from typing import Optional

class Delivery(BaseModel):
    id: int
    order_id: int
    driver_name: str
    driver_phone: str
    pickup_address: str
    delivery_address: str
    status: str  # assigned, picked_up, on_the_way, delivered
    estimated_minutes: int
    distance_km: float

class DeliveryCreate(BaseModel):
    order_id: int
    driver_name: str
    driver_phone: str
    pickup_address: str
    delivery_address: str
    status: str = "assigned"
    estimated_minutes: int
    distance_km: float

class DeliveryUpdate(BaseModel):
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    status: Optional[str] = None
    estimated_minutes: Optional[int] = None
