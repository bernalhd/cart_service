from typing import List

from sqlalchemy.orm import Session

from cart_service.app.domain.models import (
    Cart,
    CartAlreadyExistsError,
    CartItem,
    CartItemNotFoundError,
    CartNotFoundError,
)
from cart_service.app.domain.ports.repository import CartRepository


class SqlAlchemyCartRepository(CartRepository):
    def __init__(self, session: Session):
        """Initializes the repository with a database session."""
        self.session = session

    def create_cart(self, user_id: int) -> Cart:
        """Creates a new cart for a user if no cart already exists for that user."""
        if self.session.query(Cart).filter_by(user_id=user_id).first():
            raise CartAlreadyExistsError(user_id=user_id)
        cart = Cart(user_id)
        self.session.add(cart)
        self.session.commit()
        return cart

    def remove_cart(self, user_id: int) -> bool:
        """Removes the cart for a user. Returns True if deleted, False if not found."""
        cart = (
            self.session.query(Cart).filter_by(user_id=user_id).one_or_none()
        )
        if not cart:
            return False
        self.session.delete(cart)
        self.session.commit()
        return True

    def add_item_to_cart(
        self, user_id: int, product_id: int, quantity: int, unit_price: float
    ) -> bool:
        """Adds an item to a cart for a user. If the item exists, increments its quantity."""
        cart = (
            self.session.query(Cart).filter_by(user_id=user_id).one_or_none()
        )

        if not cart:
            raise CartNotFoundError(user_id)

        existing_item = (
            self.session.query(CartItem)
            .filter_by(cart_id=cart.id, product_id=product_id)
            .one_or_none()
        )

        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price,
            )
            self.session.add(new_item)

        self.session.commit()
        return True

    def remove_item_from_cart(self, user_id: int, product_id: int) -> bool:
        """Removes an item from the cart for a user, or decreases its quantity if more than one."""
        cart = (
            self.session.query(Cart).filter_by(user_id=user_id).one_or_none()
        )
        if not cart:
            raise CartNotFoundError(user_id)

        item = (
            self.session.query(CartItem)
            .filter_by(cart_id=cart.id, product_id=product_id)
            .one_or_none()
        )
        if not item:
            raise CartItemNotFoundError(product_id, cart.id)

        if item.quantity > 1:
            item.quantity -= 1
        else:
            self.session.delete(item)
        self.session.commit()
        return True

    def get_cart(self, user_id: int) -> Cart:
        """Gets the cart for a user by user_id."""
        cart = (
            self.session.query(Cart).filter_by(user_id=user_id).one_or_none()
        )
        if not cart:
            raise CartNotFoundError(user_id)
        return cart

    def get_cart_items(self, user_id: int) -> List[CartItem]:
        """Gets all items in a cart for a user by user_id."""
        cart = (
            self.session.query(Cart).filter_by(user_id=user_id).one_or_none()
        )
        if not cart:
            raise CartNotFoundError(user_id)
        items = self.session.query(CartItem).filter_by(cart_id=cart.id).all()
        return items
