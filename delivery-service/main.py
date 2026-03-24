# delivery-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Delivery, DeliveryCreate, DeliveryUpdate
from service import DeliveryService
from typing import List

app = FastAPI(
    title="Delivery Microservice",
    version="1.0.0",
    description="Manages delivery tracking and drivers for the Food Delivery Platform"
)

delivery_service = DeliveryService()

@app.get("/")
def read_root():
    return {"message": "Delivery Microservice is running", "port": 8004}

@app.get("/api/deliveries", response_model=List[Delivery])
def get_all_deliveries():
    """Get all deliveries"""
    return delivery_service.get_all()

@app.get("/api/deliveries/status/{status}", response_model=List[Delivery])
def get_deliveries_by_status(status: str):
    """Get deliveries by status (assigned, picked_up, on_the_way, delivered)"""
    return delivery_service.get_by_status(status)

@app.get("/api/deliveries/order/{order_id}", response_model=Delivery)
def get_delivery_by_order(order_id: int):
    """Get delivery details for a specific order"""
    delivery = delivery_service.get_by_order(order_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found for this order")
    return delivery

@app.get("/api/deliveries/driver/{driver_name}", response_model=List[Delivery])
def get_deliveries_by_driver(driver_name: str):
    """Get all deliveries assigned to a specific driver"""
    return delivery_service.get_by_driver(driver_name)

@app.get("/api/deliveries/{delivery_id}", response_model=Delivery)
def get_delivery(delivery_id: int):
    """Get a delivery by ID"""
    delivery = delivery_service.get_by_id(delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

@app.post("/api/deliveries", response_model=Delivery, status_code=status.HTTP_201_CREATED)
def create_delivery(delivery: DeliveryCreate):
    """Assign a new delivery"""
    return delivery_service.create(delivery)

@app.put("/api/deliveries/{delivery_id}", response_model=Delivery)
def update_delivery(delivery_id: int, delivery: DeliveryUpdate):
    """Update delivery status or driver info"""
    updated = delivery_service.update(delivery_id, delivery)
    if not updated:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return updated

@app.delete("/api/deliveries/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_delivery(delivery_id: int):
    """Delete a delivery record"""
    success = delivery_service.delete(delivery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return None
