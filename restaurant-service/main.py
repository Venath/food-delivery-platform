# restaurant-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import Restaurant, RestaurantCreate, RestaurantUpdate
from service import RestaurantService
from typing import List

app = FastAPI(
    title="Restaurant Microservice",
    version="1.0.0",
    description="Manages restaurant listings for the Food Delivery Platform"
)

restaurant_service = RestaurantService()

@app.get("/")
def read_root():
    return {"message": "Restaurant Microservice is running", "port": 8001}

@app.get("/api/restaurants", response_model=List[Restaurant])
def get_all_restaurants():
    """Get all restaurants"""
    return restaurant_service.get_all()

@app.get("/api/restaurants/open", response_model=List[Restaurant])
def get_open_restaurants():
    """Get all currently open restaurants"""
    return restaurant_service.get_open_restaurants()

@app.get("/api/restaurants/cuisine/{cuisine_type}", response_model=List[Restaurant])
def get_by_cuisine(cuisine_type: str):
    """Get restaurants by cuisine type"""
    return restaurant_service.get_by_cuisine(cuisine_type)

@app.get("/api/restaurants/{restaurant_id}", response_model=Restaurant)
def get_restaurant(restaurant_id: int):
    """Get a restaurant by ID"""
    restaurant = restaurant_service.get_by_id(restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@app.post("/api/restaurants", response_model=Restaurant, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: RestaurantCreate):
    """Create a new restaurant"""
    return restaurant_service.create(restaurant)

@app.put("/api/restaurants/{restaurant_id}", response_model=Restaurant)
def update_restaurant(restaurant_id: int, restaurant: RestaurantUpdate):
    """Update a restaurant"""
    updated = restaurant_service.update(restaurant_id, restaurant)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

@app.delete("/api/restaurants/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(restaurant_id: int):
    """Delete a restaurant"""
    success = restaurant_service.delete(restaurant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return None
