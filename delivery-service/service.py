# delivery-service/service.py
from data_service import DeliveryMockDataService

class DeliveryService:
    def __init__(self):
        self.data_service = DeliveryMockDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, delivery_id: int):
        return self.data_service.get_by_id(delivery_id)

    def get_by_order(self, order_id: int):
        return self.data_service.get_by_order(order_id)

    def get_by_status(self, status: str):
        return self.data_service.get_by_status(status)

    def get_by_driver(self, driver_name: str):
        return self.data_service.get_by_driver(driver_name)

    def create(self, data):
        return self.data_service.add(data)

    def update(self, delivery_id: int, data):
        return self.data_service.update(delivery_id, data)

    def delete(self, delivery_id: int):
        return self.data_service.delete(delivery_id)
