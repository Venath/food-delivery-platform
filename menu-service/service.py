# menu-service/service.py
from data_service import MenuMockDataService

class MenuService:
    def __init__(self):
        self.data_service = MenuMockDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, item_id: int):
        return self.data_service.get_by_id(item_id)

    def get_by_restaurant(self, restaurant_id: int):
        return self.data_service.get_by_restaurant(restaurant_id)

    def get_by_category(self, category: str):
        return self.data_service.get_by_category(category)

    def get_available_items(self):
        return self.data_service.get_available_items()

    def create(self, data):
        return self.data_service.add(data)

    def update(self, item_id: int, data):
        return self.data_service.update(item_id, data)

    def delete(self, item_id: int):
        return self.data_service.delete(item_id)
