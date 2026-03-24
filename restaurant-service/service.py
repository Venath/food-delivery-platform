# restaurant-service/service.py
from data_service import RestaurantMockDataService

class RestaurantService:
    def __init__(self):
        self.data_service = RestaurantMockDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, restaurant_id: int):
        return self.data_service.get_by_id(restaurant_id)

    def get_open_restaurants(self):
        return self.data_service.get_open_restaurants()

    def get_by_cuisine(self, cuisine_type: str):
        return self.data_service.get_by_cuisine(cuisine_type)

    def create(self, data):
        return self.data_service.add(data)

    def update(self, restaurant_id: int, data):
        return self.data_service.update(restaurant_id, data)

    def delete(self, restaurant_id: int):
        return self.data_service.delete(restaurant_id)
