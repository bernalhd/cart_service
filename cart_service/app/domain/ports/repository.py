from abc import ABC, abstractmethod
from typing import List

from cart_service.app.domain.models import Cart, CartItem


class CartRepository(ABC):
    @abstractmethod
    def create_cart(self, user_id: int) -> Cart:
        """Creates a new cart for a user if no cart already exists for that user."""
        pass

    @abstractmethod
    def remove_cart(self, user_id: int) -> bool:
        """Removes the cart for a user. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def add_item_to_cart(
        self, user_id: int, product_id: int, quantity: int, unit_price: float
    ) -> bool:
        """Adds an item to a cart for a user. If the item exists, increments its quantity."""
        pass

    @abstractmethod
    def remove_item_from_cart(self, user_id: int, product_id: int) -> bool:
        """Removes an item from the cart for a user, or decreases its quantity if more than one."""
        pass

    @abstractmethod
    def get_cart(self, user_id: int) -> Cart:
        """Gets the cart for a user by user_id."""
        pass

    @abstractmethod
    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Gets all items in a cart for a user by user_id."""
        pass
