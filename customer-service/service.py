# customer-service/service.py
from data_service import CustomerMockDataService

class CustomerService:
    def __init__(self):
        self.data_service = CustomerMockDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, customer_id: int):
        return self.data_service.get_by_id(customer_id)

    def get_by_city(self, city: str):
        return self.data_service.get_by_city(city)

    def get_active_customers(self):
        return self.data_service.get_active_customers()

    def get_by_email(self, email: str):
        return self.data_service.get_by_email(email)

    def create(self, data):
        return self.data_service.add(data)

    def update(self, customer_id: int, data):
        return self.data_service.update(customer_id, data)

    def delete(self, customer_id: int):
        return self.data_service.delete(customer_id)
