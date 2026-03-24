# menu-service/data_service.py
from models import MenuItem

class MenuMockDataService:
    def __init__(self):
        self.menu_items = [
            MenuItem(id=1, restaurant_id=1, name="Classic Burger", description="Beef patty with lettuce, tomato, cheese", price=850.00, category="Burgers", is_available=True),
            MenuItem(id=2, restaurant_id=1, name="Cheese Burger", description="Double cheese beef patty burger", price=950.00, category="Burgers", is_available=True),
            MenuItem(id=3, restaurant_id=1, name="French Fries", description="Crispy golden fries with ketchup", price=350.00, category="Sides", is_available=True),
            MenuItem(id=4, restaurant_id=2, name="Margherita Pizza", description="Classic pizza with tomato and mozzarella", price=1200.00, category="Pizzas", is_available=True),
            MenuItem(id=5, restaurant_id=2, name="Pepperoni Pizza", description="Pizza loaded with pepperoni slices", price=1500.00, category="Pizzas", is_available=False),
            MenuItem(id=6, restaurant_id=3, name="Rice and Curry", description="Traditional Sri Lankan rice with 3 curries", price=650.00, category="Main Course", is_available=True),
            MenuItem(id=7, restaurant_id=4, name="Salmon Sushi", description="Fresh salmon nigiri sushi (6 pieces)", price=1800.00, category="Sushi", is_available=True),
        ]
        self.next_id = 8

    def get_all(self):
        return self.menu_items

    def get_by_id(self, item_id: int):
        return next((m for m in self.menu_items if m.id == item_id), None)

    def get_by_restaurant(self, restaurant_id: int):
        return [m for m in self.menu_items if m.restaurant_id == restaurant_id]

    def get_by_category(self, category: str):
        return [m for m in self.menu_items if m.category.lower() == category.lower()]

    def get_available_items(self):
        return [m for m in self.menu_items if m.is_available]

    def add(self, data):
        new = MenuItem(id=self.next_id, **data.dict())
        self.menu_items.append(new)
        self.next_id += 1
        return new

    def update(self, item_id: int, data):
        item = self.get_by_id(item_id)
        if item:
            for key, value in data.dict(exclude_unset=True).items():
                setattr(item, key, value)
            return item
        return None

    def delete(self, item_id: int):
        item = self.get_by_id(item_id)
        if item:
            self.menu_items.remove(item)
            return True
        return False
