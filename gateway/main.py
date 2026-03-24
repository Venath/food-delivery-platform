# gateway/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Any

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
# CORS Middleware (configured once centrally)
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
# All microservice URLs registered here.
# Client only needs to know port 8000.
# ─────────────────────────────────────────
SERVICES = {
    "restaurant": "http://localhost:8001",
    "menu":       "http://localhost:8002",
    "order":      "http://localhost:8003",
    "delivery":   "http://localhost:8004",
    "customer":   "http://localhost:8005",
}

# ─────────────────────────────────────────
# CORE FORWARDING FUNCTION
# Receives request → finds service → forwards → returns response
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
    """Gateway root - shows all available services"""
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
    """Gateway health check"""
    return {"status": "healthy", "service": "api-gateway", "port": 8000}


# ─────────────────────────────────────────
# RESTAURANT ROUTES  (forwards to port 8001)
# ─────────────────────────────────────────
@app.get("/gateway/restaurants", tags=["Restaurant Service"])
async def get_all_restaurants():
    """Get all restaurants — via Gateway → Restaurant Service (8001)"""
    return await forward_request("restaurant", "/api/restaurants", "GET")

@app.get("/gateway/restaurants/open", tags=["Restaurant Service"])
async def get_open_restaurants():
    """Get all open restaurants — via Gateway → Restaurant Service (8001)"""
    return await forward_request("restaurant", "/api/restaurants/open", "GET")

@app.get("/gateway/restaurants/cuisine/{cuisine_type}", tags=["Restaurant Service"])
async def get_restaurants_by_cuisine(cuisine_type: str):
    """Get restaurants by cuisine type — via Gateway → Restaurant Service (8001)"""
    return await forward_request("restaurant", f"/api/restaurants/cuisine/{cuisine_type}", "GET")

@app.get("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def get_restaurant(restaurant_id: int):
    """Get restaurant by ID — via Gateway → Restaurant Service (8001)"""
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "GET")

@app.post("/gateway/restaurants", tags=["Restaurant Service"])
async def create_restaurant(request: Request):
    """Create a new restaurant — via Gateway → Restaurant Service (8001)"""
    body = await request.json()
    return await forward_request("restaurant", "/api/restaurants", "POST", json=body)

@app.put("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def update_restaurant(restaurant_id: int, request: Request):
    """Update a restaurant — via Gateway → Restaurant Service (8001)"""
    body = await request.json()
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "PUT", json=body)

@app.delete("/gateway/restaurants/{restaurant_id}", tags=["Restaurant Service"])
async def delete_restaurant(restaurant_id: int):
    """Delete a restaurant — via Gateway → Restaurant Service (8001)"""
    return await forward_request("restaurant", f"/api/restaurants/{restaurant_id}", "DELETE")


# ─────────────────────────────────────────
# MENU ROUTES  (forwards to port 8002)
# ─────────────────────────────────────────
@app.get("/gateway/menus", tags=["Menu Service"])
async def get_all_menus():
    """Get all menu items — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", "/api/menus", "GET")

@app.get("/gateway/menus/available", tags=["Menu Service"])
async def get_available_menu_items():
    """Get available menu items — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", "/api/menus/available", "GET")

@app.get("/gateway/menus/restaurant/{restaurant_id}", tags=["Menu Service"])
async def get_menu_by_restaurant(restaurant_id: int):
    """Get menu items by restaurant — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", f"/api/menus/restaurant/{restaurant_id}", "GET")

@app.get("/gateway/menus/category/{category}", tags=["Menu Service"])
async def get_menu_by_category(category: str):
    """Get menu items by category — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", f"/api/menus/category/{category}", "GET")

@app.get("/gateway/menus/{item_id}", tags=["Menu Service"])
async def get_menu_item(item_id: int):
    """Get menu item by ID — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", f"/api/menus/{item_id}", "GET")

@app.post("/gateway/menus", tags=["Menu Service"])
async def create_menu_item(request: Request):
    """Create a menu item — via Gateway → Menu Service (8002)"""
    body = await request.json()
    return await forward_request("menu", "/api/menus", "POST", json=body)

@app.put("/gateway/menus/{item_id}", tags=["Menu Service"])
async def update_menu_item(item_id: int, request: Request):
    """Update a menu item — via Gateway → Menu Service (8002)"""
    body = await request.json()
    return await forward_request("menu", f"/api/menus/{item_id}", "PUT", json=body)

@app.delete("/gateway/menus/{item_id}", tags=["Menu Service"])
async def delete_menu_item(item_id: int):
    """Delete a menu item — via Gateway → Menu Service (8002)"""
    return await forward_request("menu", f"/api/menus/{item_id}", "DELETE")


# ─────────────────────────────────────────
# ORDER ROUTES  (forwards to port 8003)
# ─────────────────────────────────────────
@app.get("/gateway/orders", tags=["Order Service"])
async def get_all_orders():
    """Get all orders — via Gateway → Order Service (8003)"""
    return await forward_request("order", "/api/orders", "GET")

@app.get("/gateway/orders/status/{status}", tags=["Order Service"])
async def get_orders_by_status(status: str):
    """Get orders by status — via Gateway → Order Service (8003)"""
    return await forward_request("order", f"/api/orders/status/{status}", "GET")

@app.get("/gateway/orders/customer/{customer_id}", tags=["Order Service"])
async def get_orders_by_customer(customer_id: int):
    """Get orders by customer — via Gateway → Order Service (8003)"""
    return await forward_request("order", f"/api/orders/customer/{customer_id}", "GET")

@app.get("/gateway/orders/restaurant/{restaurant_id}", tags=["Order Service"])
async def get_orders_by_restaurant(restaurant_id: int):
    """Get orders by restaurant — via Gateway → Order Service (8003)"""
    return await forward_request("order", f"/api/orders/restaurant/{restaurant_id}", "GET")

@app.get("/gateway/orders/{order_id}", tags=["Order Service"])
async def get_order(order_id: int):
    """Get order by ID — via Gateway → Order Service (8003)"""
    return await forward_request("order", f"/api/orders/{order_id}", "GET")

@app.post("/gateway/orders", tags=["Order Service"])
async def create_order(request: Request):
    """Place a new order — via Gateway → Order Service (8003)"""
    body = await request.json()
    return await forward_request("order", "/api/orders", "POST", json=body)

@app.put("/gateway/orders/{order_id}", tags=["Order Service"])
async def update_order(order_id: int, request: Request):
    """Update order status — via Gateway → Order Service (8003)"""
    body = await request.json()
    return await forward_request("order", f"/api/orders/{order_id}", "PUT", json=body)

@app.delete("/gateway/orders/{order_id}", tags=["Order Service"])
async def delete_order(order_id: int):
    """Cancel an order — via Gateway → Order Service (8003)"""
    return await forward_request("order", f"/api/orders/{order_id}", "DELETE")


# ─────────────────────────────────────────
# DELIVERY ROUTES  (forwards to port 8004)
# ─────────────────────────────────────────
@app.get("/gateway/deliveries", tags=["Delivery Service"])
async def get_all_deliveries():
    """Get all deliveries — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", "/api/deliveries", "GET")

@app.get("/gateway/deliveries/status/{status}", tags=["Delivery Service"])
async def get_deliveries_by_status(status: str):
    """Get deliveries by status — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", f"/api/deliveries/status/{status}", "GET")

@app.get("/gateway/deliveries/order/{order_id}", tags=["Delivery Service"])
async def get_delivery_by_order(order_id: int):
    """Track delivery by order ID — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", f"/api/deliveries/order/{order_id}", "GET")

@app.get("/gateway/deliveries/driver/{driver_name}", tags=["Delivery Service"])
async def get_deliveries_by_driver(driver_name: str):
    """Get deliveries by driver — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", f"/api/deliveries/driver/{driver_name}", "GET")

@app.get("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def get_delivery(delivery_id: int):
    """Get delivery by ID — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "GET")

@app.post("/gateway/deliveries", tags=["Delivery Service"])
async def create_delivery(request: Request):
    """Assign a new delivery — via Gateway → Delivery Service (8004)"""
    body = await request.json()
    return await forward_request("delivery", "/api/deliveries", "POST", json=body)

@app.put("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def update_delivery(delivery_id: int, request: Request):
    """Update delivery status — via Gateway → Delivery Service (8004)"""
    body = await request.json()
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "PUT", json=body)

@app.delete("/gateway/deliveries/{delivery_id}", tags=["Delivery Service"])
async def delete_delivery(delivery_id: int):
    """Delete a delivery record — via Gateway → Delivery Service (8004)"""
    return await forward_request("delivery", f"/api/deliveries/{delivery_id}", "DELETE")


# ─────────────────────────────────────────
# CUSTOMER ROUTES  (forwards to port 8005)
# ─────────────────────────────────────────
@app.get("/gateway/customers", tags=["Customer Service"])
async def get_all_customers():
    """Get all customers — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", "/api/customers", "GET")

@app.get("/gateway/customers/active", tags=["Customer Service"])
async def get_active_customers():
    """Get active customers — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", "/api/customers/active", "GET")

@app.get("/gateway/customers/city/{city}", tags=["Customer Service"])
async def get_customers_by_city(city: str):
    """Get customers by city — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", f"/api/customers/city/{city}", "GET")

@app.get("/gateway/customers/email/{email}", tags=["Customer Service"])
async def get_customer_by_email(email: str):
    """Get customer by email — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", f"/api/customers/email/{email}", "GET")

@app.get("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def get_customer(customer_id: int):
    """Get customer by ID — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", f"/api/customers/{customer_id}", "GET")

@app.post("/gateway/customers", tags=["Customer Service"])
async def create_customer(request: Request):
    """Register a new customer — via Gateway → Customer Service (8005)"""
    body = await request.json()
    return await forward_request("customer", "/api/customers", "POST", json=body)

@app.put("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def update_customer(customer_id: int, request: Request):
    """Update customer profile — via Gateway → Customer Service (8005)"""
    body = await request.json()
    return await forward_request("customer", f"/api/customers/{customer_id}", "PUT", json=body)

@app.delete("/gateway/customers/{customer_id}", tags=["Customer Service"])
async def delete_customer(customer_id: int):
    """Delete a customer — via Gateway → Customer Service (8005)"""
    return await forward_request("customer", f"/api/customers/{customer_id}", "DELETE")
