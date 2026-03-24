# menu-service/main.py
from fastapi import FastAPI, HTTPException, status
from models import MenuItem, MenuItemCreate, MenuItemUpdate
from service import MenuService
from typing import List

app = FastAPI(
    title="Menu Microservice",
    version="1.0.0",
    description="Manages menu items for restaurants in the Food Delivery Platform"
)

menu_service = MenuService()

@app.get("/")
def read_root():
    return {"message": "Menu Microservice is running", "port": 8002}

@app.get("/api/menus", response_model=List[MenuItem])
def get_all_menu_items():
    """Get all menu items"""
    return menu_service.get_all()

@app.get("/api/menus/available", response_model=List[MenuItem])
def get_available_items():
    """Get all currently available menu items"""
    return menu_service.get_available_items()

@app.get("/api/menus/restaurant/{restaurant_id}", response_model=List[MenuItem])
def get_menu_by_restaurant(restaurant_id: int):
    """Get all menu items for a specific restaurant"""
    return menu_service.get_by_restaurant(restaurant_id)

@app.get("/api/menus/category/{category}", response_model=List[MenuItem])
def get_menu_by_category(category: str):
    """Get menu items by category"""
    return menu_service.get_by_category(category)

@app.get("/api/menus/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: int):
    """Get a menu item by ID"""
    item = menu_service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@app.post("/api/menus", response_model=MenuItem, status_code=status.HTTP_201_CREATED)
def create_menu_item(item: MenuItemCreate):
    """Create a new menu item"""
    return menu_service.create(item)

@app.put("/api/menus/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: int, item: MenuItemUpdate):
    """Update a menu item"""
    updated = menu_service.update(item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

@app.delete("/api/menus/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(item_id: int):
    """Delete a menu item"""
    success = menu_service.delete(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return None
