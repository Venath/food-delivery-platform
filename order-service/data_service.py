# order-service/data_service.py
from models import Order, OrderItem

class OrderMockDataService:
    def __init__(self):
        self.orders = [
            Order(
                id=1,
                customer_id=1,
                restaurant_id=1,
                items=[
                    OrderItem(menu_item_id=1, menu_item_name="Classic Burger", quantity=2, unit_price=850.00, subtotal=1700.00),
                    OrderItem(menu_item_id=3, menu_item_name="French Fries", quantity=1, unit_price=350.00, subtotal=350.00),
                ],
                total_amount=2050.00,
                status="delivered",
                delivery_address="10 Park Ave, Colombo 3",
                notes="Extra ketchup please"
            ),
            Order(
                id=2,
                customer_id=2,
                restaurant_id=2,
                items=[
                    OrderItem(menu_item_id=4, menu_item_name="Margherita Pizza", quantity=1, unit_price=1200.00, subtotal=1200.00),
                ],
                total_amount=1200.00,
                status="preparing",
                delivery_address="55 Flower Rd, Colombo 7",
                notes=None
            ),
            Order(
                id=3,
                customer_id=3,
                restaurant_id=4,
                items=[
                    OrderItem(menu_item_id=7, menu_item_name="Salmon Sushi", quantity=2, unit_price=1800.00, subtotal=3600.00),
                ],
                total_amount=3600.00,
                status="pending",
                delivery_address="22 Sea View Rd, Colombo 1",
                notes="Ring doorbell twice"
            ),
        ]
        self.next_id = 4

    def get_all(self):
        return self.orders

    def get_by_id(self, order_id: int):
        return next((o for o in self.orders if o.id == order_id), None)

    def get_by_customer(self, customer_id: int):
        return [o for o in self.orders if o.customer_id == customer_id]

    def get_by_restaurant(self, restaurant_id: int):
        return [o for o in self.orders if o.restaurant_id == restaurant_id]

    def get_by_status(self, status: str):
        return [o for o in self.orders if o.status.lower() == status.lower()]

    def add(self, data):
        new = Order(id=self.next_id, status="pending", **data.dict())
        self.orders.append(new)
        self.next_id += 1
        return new

    def update(self, order_id: int, data):
        order = self.get_by_id(order_id)
        if order:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(order, key, value)
            return order
        return None

    def delete(self, order_id: int):
        order = self.get_by_id(order_id)
        if order:
            self.orders.remove(order)
            return True
        return False
