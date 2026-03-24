# order-service/service.py
from data_service import OrderMockDataService

class OrderService:
    def __init__(self):
        self.data_service = OrderMockDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, order_id: int):
        return self.data_service.get_by_id(order_id)

    def get_by_customer(self, customer_id: int):
        return self.data_service.get_by_customer(customer_id)

    def get_by_restaurant(self, restaurant_id: int):
        return self.data_service.get_by_restaurant(restaurant_id)

    def get_by_status(self, status: str):
        return self.data_service.get_by_status(status)

    def create(self, data):
        return self.data_service.add(data)

    def update(self, order_id: int, data):
        return self.data_service.update(order_id, data)

    def delete(self, order_id: int):
        return self.data_service.delete(order_id)
