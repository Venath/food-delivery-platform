# customer-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from service import CustomerService
from typing import List

app = FastAPI(
    title="Customer Microservice",
    version="1.0.0",
    description="Manages customer profiles for the Food Delivery Platform"
)

customer_service = CustomerService()

@app.get("/")
def read_root():
    return {"message": "Customer Microservice is running", "port": 8005}

@app.get("/api/customers", response_model=List[Customer])
def get_all_customers():
    """Get all customers"""
    return customer_service.get_all()

@app.get("/api/customers/active", response_model=List[Customer])
def get_active_customers():
    """Get all active customers"""
    return customer_service.get_active_customers()

@app.get("/api/customers/city/{city}", response_model=List[Customer])
def get_customers_by_city(city: str):
    """Get customers by city"""
    return customer_service.get_by_city(city)

@app.get("/api/customers/email/{email}", response_model=Customer)
def get_customer_by_email(email: str):
    """Get a customer by email address"""
    customer = customer_service.get_by_email(email)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/api/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    """Get a customer by ID"""
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/api/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    """Register a new customer"""
    return customer_service.create(customer)

@app.put("/api/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate):
    """Update customer profile"""
    updated = customer_service.update(customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated

@app.delete("/api/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    """Delete a customer"""
    success = customer_service.delete(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None
