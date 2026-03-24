# restaurant-service/data_service.py
from models import Restaurant

class RestaurantMockDataService:
    def __init__(self):
        self.restaurants = [
            Restaurant(id=1, name="Burger Palace", address="123 Main St, Colombo", phone="0112345678", cuisine_type="Fast Food", rating=4.5, is_open=True),
            Restaurant(id=2, name="Pizza Heaven", address="456 Galle Rd, Colombo", phone="0119876543", cuisine_type="Italian", rating=4.2, is_open=True),
            Restaurant(id=3, name="Spice Garden", address="789 Kandy Rd, Colombo", phone="0111122334", cuisine_type="Sri Lankan", rating=4.8, is_open=False),
            Restaurant(id=4, name="Sushi World", address="321 Marine Dr, Colombo", phone="0115566778", cuisine_type="Japanese", rating=4.6, is_open=True),
        ]
        self.next_id = 5

    def get_all(self):
        return self.restaurants

    def get_by_id(self, restaurant_id: int):
        return next((r for r in self.restaurants if r.id == restaurant_id), None)

    def get_open_restaurants(self):
        return [r for r in self.restaurants if r.is_open]

    def get_by_cuisine(self, cuisine_type: str):
        return [r for r in self.restaurants if r.cuisine_type.lower() == cuisine_type.lower()]

    def add(self, data):
        new = Restaurant(id=self.next_id, **data.dict())
        self.restaurants.append(new)
        self.next_id += 1
        return new

    def update(self, restaurant_id: int, data):
        restaurant = self.get_by_id(restaurant_id)
        if restaurant:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(restaurant, key, value)
            return restaurant
        return None

    def delete(self, restaurant_id: int):
        restaurant = self.get_by_id(restaurant_id)
        if restaurant:
            self.restaurants.remove(restaurant)
            return True
        return False
