# 🍔 Food Delivery Platform — Microservices Architecture
## IT4020 Assignment 2 | SLIIT | 2026

---

## 📁 Project Structure

```
food-delivery-platform/
├── gateway/                  → API Gateway (Port 8000)
├── restaurant-service/       → Restaurant Service (Port 8001) - Member 1
├── menu-service/             → Menu Service (Port 8002)        - Member 2
├── order-service/            → Order Service (Port 8003)       - Member 3
├── delivery-service/         → Delivery Service (Port 4)      - Member 4
├── customer-service/         → Customer Service (Port 8005)    - Member 5
└── requirements.txt
```

---

## 🚀 How to Run

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run each microservice (open separate terminals)
```bash
# Terminal 1 - Restaurant Service
cd restaurant-service
uvicorn main:app --reload --port 8001

# Terminal 2 - Menu Service
cd menu-service
uvicorn main:app --reload --port 8002

# Terminal 3 - Order Service
cd order-service
uvicorn main:app --reload --port 8003

# Terminal 4 - Delivery Service
cd delivery-service
uvicorn main:app --reload --port 8004

# Terminal 5 - Customer Service
cd customer-service
uvicorn main:app --reload --port 8005

# Terminal 6 - API Gateway
cd gateway
uvicorn main:app --reload --port 8000
```

---

## 🌐 Swagger URLs

### Direct (Native) Access:
| Service            | Swagger URL                        |
|--------------------|------------------------------------|
| Restaurant Service | http://localhost:8001/docs         |
| Menu Service       | http://localhost:8002/docs         |
| Order Service      | http://localhost:8003/docs         |
| Delivery Service   | http://localhost:8004/docs         |
| Customer Service   | http://localhost:8005/docs         |

### Via API Gateway:
| Service            | Gateway URL                        |
|--------------------|------------------------------------|
| All Services       | http://localhost:8000/docs         |
| Restaurants        | http://localhost:8000/gateway/restaurants |
| Menus              | http://localhost:8000/gateway/menus       |
| Orders             | http://localhost:8000/gateway/orders      |
| Deliveries         | http://localhost:8000/gateway/deliveries  |
| Customers          | http://localhost:8000/gateway/customers   |
