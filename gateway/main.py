# gateway/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Optional, List
import httpx

app = FastAPI(
    title="Food Delivery Platform - API Gateway",
    version="1.0.0",
    description="""
    ## API Gateway for Food Delivery Platform
    
    This gateway provides a **single entry point** for all microservices.
    Instead of calling each service on its own port, all requests go through port **8000**.
    
    ### Microservices Connected:
    | Service             | Internal Port | Gateway Prefix         |
    |---------------------|---------------|------------------------|
    | Restaurant Service  | 8001          | /gateway/restaurants   |
    | Menu Service        | 8002          | /gateway/menus         |
    | Order Service       | 8003          | /gateway/orders        |
    | Delivery Service    | 8004          | /gateway/deliveries    |
    | Customer Service    | 8005          | /gateway/customers     |
    """
)

# ─────────────────────────────────────────
# CORS Middleware
# ─────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# SERVICE REGISTRY
# ─────────────────────────────────────────
SERVICES = {
    "restaurant": "http://localhost:8001",
    "menu":       "http://localhost:8002",
    "order":      "http://localhost:8003",
    "delivery":   "http://localhost:8004",
    "customer":   "http://localhost:8005",
}

# ─────────────────────────────────────────
# PYDANTIC MODELS FOR GATEWAY
# Required so Swagger UI shows JSON input fields
# ─────────────────────────────────────────

# --- Restaurant Models ---
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

# --- Menu Models ---
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

# --- Order Models ---
class OrderItem(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    unit_price: float
    subtotal: float

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

# --- Delivery Models ---
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

# --- Customer Models ---
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


# ─────────────────────────────────────────
# CORE FORWARDING FUNCTION
# ─────────────────────────────────────────
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail=f"Service '{service}' not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"Service '{service}' timed out")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service '{service}' is unavailable: {str(e)}")


# ─────────────────────────────────────────
# ROOT & HEALTH CHECK
# ─────────────────────────────────────────
@app.get("/", tags=["Gateway Info"])
def read_root():
    return {
        "message": "Food Delivery Platform - API Gateway is running",
        "version": "1.0.0",
        "port": 8000,
        "docs": "http://localhost:8000/docs",
        "registered_services": {
            name: f"{url}  →  /gateway/{name}s"
            for name, url in SERVICES.items()
        }
    }

@app.get("/health", tags=["Gateway Info"])
def health_check():
    return {"status": "healthy", "service": "api-gateway", "port": 8000}


# ─────────────────────────────────────────
# RESTAURANT ROUTES  (forwards to port 8001)
# ─────────────────────────────────────────
@app.get("/gateway/restaurants", tags=["Restaurant Service"])
async def get_all_restaurants():
    """Get all restaurants"""
    return await forward_request("restaurant", "/api/restaurants", "GET")

@app.get("/gateway/restaurants/open", tags=["Restaurant Service"])
async def get_open_restaurants():
    """Get all open restaurants"""
    return await forward_request("restaurant", "/api/restaurants/open", "GET")

@app.get("/gateway/restaurants/cuisine/{cuisine_type}", tags=["Restaurant Service"])
async def get_restaurants_by_cuisine(cuisine_type: str):
    """Get restaurants by cuisine type"""
    return await forward_request("restaurant", f"/api/restaurants/cuisine/{cuisine_type}", "GET")

@app.get("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def get_restaurant(restaurant_id: int):
    """Get restaurant by ID"""
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "GET")

@app.post("/gateway/restaurants", tags=["Restaurant Service"])
async def create_restaurant(body: RestaurantCreate):
    """Create a new restaurant"""
    return await forward_request("restaurant", "/api/restaurants", "POST", json=body.dict())

@app.put("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def update_restaurant(restaurant_id: int, body: RestaurantUpdate):
    """Update a restaurant"""
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def delete_restaurant(restaurant_id: int):
    """Delete a restaurant"""
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "DELETE")


# ─────────────────────────────────────────
# MENU ROUTES  (forwards to port 8002)
# ─────────────────────────────────────────
@app.get("/gateway/menus", tags=["Menu Service"])
async def get_all_menus():
    """Get all menu items"""
    return await forward_request("menu", "/api/menus", "GET")

@app.get("/gateway/menus/available", tags=["Menu Service"])
async def get_available_menu_items():
    """Get available menu items"""
    return await forward_request("menu", "/api/menus/available", "GET")

@app.get("/gateway/menus/restaurant/{restaurant_id}", tags=["Menu Service"])
async def get_menu_by_restaurant(restaurant_id: int):
    """Get menu items by restaurant ID"""
    return await forward_request("menu", f"/api/menus/restaurant/{restaurant_id}", "GET")

@app.get("/gateway/menus/category/{category}", tags=["Menu Service"])
async def get_menu_by_category(category: str):
    """Get menu items by category"""
    return await forward_request("menu", f"/api/menus/category/{category}", "GET")

@app.get("/gateway/menus/{item_id}", tags=["Menu Service"])
async def get_menu_item(item_id: int):
    """Get menu item by ID"""
    return await forward_request("menu", f"/api/menus/{item_id}", "GET")

@app.post("/gateway/menus", tags=["Menu Service"])
async def create_menu_item(body: MenuItemCreate):
    """Create a new menu item"""
    return await forward_request("menu", "/api/menus", "POST", json=body.dict())

@app.put("/gateway/menus/{item_id}", tags=["Menu Service"])
async def update_menu_item(item_id: int, body: MenuItemUpdate):
    """Update a menu item"""
    return await forward_request("menu", f"/api/menus/{item_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/menus/{item_id}", tags=["Menu Service"])
async def delete_menu_item(item_id: int):
    """Delete a menu item"""
    return await forward_request("menu", f"/api/menus/{item_id}", "DELETE")


# ─────────────────────────────────────────
# ORDER ROUTES  (forwards to port 8003)
# ─────────────────────────────────────────
@app.get("/gateway/orders", tags=["Order Service"])
async def get_all_orders():
    """Get all orders"""
    return await forward_request("order", "/api/orders", "GET")

@app.get("/gateway/orders/status/{status}", tags=["Order Service"])
async def get_orders_by_status(status: str):
    """Get orders by status (pending, confirmed, preparing, out_for_delivery, delivered, cancelled)"""
    return await forward_request("order", f"/api/orders/status/{status}", "GET")

@app.get("/gateway/orders/customer/{customer_id}", tags=["Order Service"])
async def get_orders_by_customer(customer_id: int):
    """Get orders by customer ID"""
    return await forward_request("order", f"/api/orders/customer/{customer_id}", "GET")

@app.get("/gateway/orders/restaurant/{restaurant_id}", tags=["Order Service"])
async def get_orders_by_restaurant(restaurant_id: int):
    """Get orders by restaurant ID"""
    return await forward_request("order", f"/api/orders/restaurant/{restaurant_id}", "GET")

@app.get("/gateway/orders/{order_id}", tags=["Order Service"])
async def get_order(order_id: int):
    """Get order by ID"""
    return await forward_request("order", f"/api/orders/{order_id}", "GET")

@app.post("/gateway/orders", tags=["Order Service"])
async def create_order(body: OrderCreate):
    """Place a new food order"""
    return await forward_request("order", "/api/orders", "POST", json=body.dict())

@app.put("/gateway/orders/{order_id}", tags=["Order Service"])
async def update_order(order_id: int, body: OrderUpdate):
    """Update order status"""
    return await forward_request("order", f"/api/orders/{order_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/orders/{order_id}", tags=["Order Service"])
async def delete_order(order_id: int):
    """Cancel an order"""
    return await forward_request("order", f"/api/orders/{order_id}", "DELETE")


# ─────────────────────────────────────────
# DELIVERY ROUTES  (forwards to port 8004)
# ─────────────────────────────────────────
@app.get("/gateway/deliveries", tags=["Delivery Service"])
async def get_all_deliveries():
    """Get all deliveries"""
    return await forward_request("delivery", "/api/deliveries", "GET")

@app.get("/gateway/deliveries/status/{status}", tags=["Delivery Service"])
async def get_deliveries_by_status(status: str):
    """Get deliveries by status (assigned, picked_up, on_the_way, delivered)"""
    return await forward_request("delivery", f"/api/deliveries/status/{status}", "GET")

@app.get("/gateway/deliveries/order/{order_id}", tags=["Delivery Service"])
async def get_delivery_by_order(order_id: int):
    """Track delivery by order ID"""
    return await forward_request("delivery", f"/api/deliveries/order/{order_id}", "GET")

@app.get("/gateway/deliveries/driver/{driver_name}", tags=["Delivery Service"])
async def get_deliveries_by_driver(driver_name: str):
    """Get deliveries by driver name"""
    return await forward_request("delivery", f"/api/deliveries/driver/{driver_name}", "GET")

@app.get("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def get_delivery(delivery_id: int):
    """Get delivery by ID"""
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "GET")

@app.post("/gateway/deliveries", tags=["Delivery Service"])
async def create_delivery(body: DeliveryCreate):
    """Assign a new delivery"""
    return await forward_request("delivery", "/api/deliveries", "POST", json=body.dict())

@app.put("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def update_delivery(delivery_id: int, body: DeliveryUpdate):
    """Update delivery status or driver info"""
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def delete_delivery(delivery_id: int):
    """Delete a delivery record"""
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "DELETE")


# ─────────────────────────────────────────
# CUSTOMER ROUTES  (forwards to port 8005)
# ─────────────────────────────────────────
@app.get("/gateway/customers", tags=["Customer Service"])
async def get_all_customers():
    """Get all customers"""
    return await forward_request("customer", "/api/customers", "GET")

@app.get("/gateway/customers/active", tags=["Customer Service"])
async def get_active_customers():
    """Get all active customers"""
    return await forward_request("customer", "/api/customers/active", "GET")

@app.get("/gateway/customers/city/{city}", tags=["Customer Service"])
async def get_customers_by_city(city: str):
    """Get customers by city"""
    return await forward_request("customer", f"/api/customers/city/{city}", "GET")

@app.get("/gateway/customers/email/{email}", tags=["Customer Service"])
async def get_customer_by_email(email: str):
    """Get customer by email address"""
    return await forward_request("customer", f"/api/customers/email/{email}", "GET")

@app.get("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def get_customer(customer_id: int):
    """Get customer by ID"""
    return await forward_request("customer", f"/api/customers/{customer_id}", "GET")

@app.post("/gateway/customers", tags=["Customer Service"])
async def create_customer(body: CustomerCreate):
    """Register a new customer"""
    return await forward_request("customer", "/api/customers", "POST", json=body.dict())

@app.put("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def update_customer(customer_id: int, body: CustomerUpdate):
    """Update customer profile"""
    return await forward_request("customer", f"/api/customers/{customer_id}", "PUT", json=body.dict(exclude_unset=True))

@app.delete("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def delete_customer(customer_id: int):
    """Delete a customer"""
    return await forward_request("customer", f"/api/customers/{customer_id}", "DELETE")
