# order-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Order, OrderCreate, OrderUpdate
from service import OrderService
from typing import List

app = FastAPI(
    title="Order Microservice",
    version="1.0.0",
    description="Manages food orders for the Food Delivery Platform"
)

order_service = OrderService()

@app.get("/")
def read_root():
    return {"message": "Order Microservice is running", "port": 8003}

@app.get("/api/orders", response_model=List[Order])
def get_all_orders():
    """Get all orders"""
    return order_service.get_all()

@app.get("/api/orders/status/{status}", response_model=List[Order])
def get_orders_by_status(status: str):
    """Get orders by status (pending, confirmed, preparing, out_for_delivery, delivered, cancelled)"""
    return order_service.get_by_status(status)

@app.get("/api/orders/customer/{customer_id}", response_model=List[Order])
def get_orders_by_customer(customer_id: int):
    """Get all orders for a specific customer"""
    return order_service.get_by_customer(customer_id)

@app.get("/api/orders/restaurant/{restaurant_id}", response_model=List[Order])
def get_orders_by_restaurant(restaurant_id: int):
    """Get all orders for a specific restaurant"""
    return order_service.get_by_restaurant(restaurant_id)

@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """Get an order by ID"""
    order = order_service.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post("/api/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """Place a new food order"""
    return order_service.create(order)

@app.put("/api/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: OrderUpdate):
    """Update order status"""
    updated = order_service.update(order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@app.delete("/api/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    """Cancel/delete an order"""
    success = order_service.delete(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return None
