# delivery-service/data_service.py
from models import Delivery

class DeliveryMockDataService:
    def __init__(self):
        self.deliveries = [
            Delivery(id=1, order_id=1, driver_name="Kamal Perera", driver_phone="0771234567", pickup_address="123 Main St, Colombo", delivery_address="10 Park Ave, Colombo 3", status="delivered", estimated_minutes=30, distance_km=3.5),
            Delivery(id=2, order_id=2, driver_name="Nimal Silva", driver_phone="0779876543", pickup_address="456 Galle Rd, Colombo", delivery_address="55 Flower Rd, Colombo 7", status="on_the_way", estimated_minutes=20, distance_km=2.8),
            Delivery(id=3, order_id=3, driver_name="Sunil Fernando", driver_phone="0775566778", pickup_address="321 Marine Dr, Colombo", delivery_address="22 Sea View Rd, Colombo 1", status="assigned", estimated_minutes=45, distance_km=5.2),
        ]
        self.next_id = 4

    def get_all(self):
        return self.deliveries

    def get_by_id(self, delivery_id: int):
        return next((d for d in self.deliveries if d.id == delivery_id), None)

    def get_by_order(self, order_id: int):
        return next((d for d in self.deliveries if d.order_id == order_id), None)

    def get_by_status(self, status: str):
        return [d for d in self.deliveries if d.status.lower() == status.lower()]

    def get_by_driver(self, driver_name: str):
        return [d for d in self.deliveries if driver_name.lower() in d.driver_name.lower()]

    def add(self, data):
        new = Delivery(id=self.next_id, **data.dict())
        self.deliveries.append(new)
        self.next_id += 1
        return new

    def update(self, delivery_id: int, data):
        delivery = self.get_by_id(delivery_id)
        if delivery:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(delivery, key, value)
            return delivery
        return None

    def delete(self, delivery_id: int):
        delivery = self.get_by_id(delivery_id)
        if delivery:
            self.deliveries.remove(delivery)
            return True
        return False
