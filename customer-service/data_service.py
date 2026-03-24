# customer-service/data_service.py
from models import Customer

class CustomerMockDataService:
    def __init__(self):
        self.customers = [
            Customer(id=1, name="Ashan Perera", email="ashan@gmail.com", phone="0771234567", address="10 Park Ave", city="Colombo 3", is_active=True),
            Customer(id=2, name="Dilani Silva", email="dilani@gmail.com", phone="0779876543", address="55 Flower Rd", city="Colombo 7", is_active=True),
            Customer(id=3, name="Ruwan Fernando", email="ruwan@gmail.com", phone="0775566778", address="22 Sea View Rd", city="Colombo 1", is_active=True),
            Customer(id=4, name="Nimasha Jayawardena", email="nimasha@gmail.com", phone="0773344556", address="88 High Level Rd", city="Nugegoda", is_active=False),
            Customer(id=5, name="Tharindu Bandara", email="tharindu@gmail.com", phone="0770011223", address="15 Station Rd", city="Maharagama", is_active=True),
        ]
        self.next_id = 6

    def get_all(self):
        return self.customers

    def get_by_id(self, customer_id: int):
        return next((c for c in self.customers if c.id == customer_id), None)

    def get_by_city(self, city: str):
        return [c for c in self.customers if city.lower() in c.city.lower()]

    def get_active_customers(self):
        return [c for c in self.customers if c.is_active]

    def get_by_email(self, email: str):
        return next((c for c in self.customers if c.email.lower() == email.lower()), None)

    def add(self, data):
        new = Customer(id=self.next_id, **data.dict())
        self.customers.append(new)
        self.next_id += 1
        return new

    def update(self, customer_id: int, data):
        customer = self.get_by_id(customer_id)
        if customer:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(customer, key, value)
            return customer
        return None

    def delete(self, customer_id: int):
        customer = self.get_by_id(customer_id)
        if customer:
            self.customers.remove(customer)
            return True
        return False
