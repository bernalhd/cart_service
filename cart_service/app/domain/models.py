from dataclasses import dataclass, field
from typing import List


@dataclass
class CartItem:
    cart_id: int
    product_id: int
    quantity: int
    unit_price: float


@dataclass
class Cart:
    user_id: int
    items: List[CartItem] = field(default_factory=list)


# CreateCart
@dataclass
class CreateCartRequest:
    user_id: int


@dataclass
class CreateCartResponse:
    cart_id: int


# RemoveCart
@dataclass
class RemoveCartRequest:
    cart_id: int


@dataclass
class RemoveCartResponse:
    success: bool


# AddToCart
@dataclass
class AddToCartRequest:
    cart_id: int
    product_id: int
    quantity: int
    unit_price: float


@dataclass
class AddToCartResponse:
    success: bool


# RemoveFromCart
@dataclass
class RemoveFromCartRequest:
    cart_id: int
    product_id: int


@dataclass
class RemoveFromCartResponse:
    success: bool


# GetCart
@dataclass
class GetCartRequest:
    cart_id: int


@dataclass
class GetCartResponse:
    cart: Cart
    items: list[CartItem]
    total: float


# Exceptions
class CartError(Exception):
    pass


class CartNotFoundError(CartError):
    def __init__(self, cart_id: int):
        super().__init__(f"Cart with ID {cart_id} not found.")


class CartItemNotFoundError(CartError):
    def __init__(self, product_id: int, cart_id: int):
        super().__init__(
            f"Product with ID {product_id} not found in cart {cart_id}."
        )


class CartAlreadyExistsError(CartError):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} already has a cart.")
