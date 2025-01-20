from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from cart_service.app.domain.models import Cart, CartItem
from cart_service.app.infrastructure.db_config import db_config

metadata = db_config.get_metadata()
mapper_registry = db_config.get_mapper_registry()

carts_table = Table(
    "carts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False, unique=True),
)

cart_items_table = Table(
    "cart_items",
    metadata,
    Column(
        "cart_id",
        Integer,
        ForeignKey("carts.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("product_id", Integer, nullable=False, primary_key=True),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Integer, nullable=False),
)


def start_mappers():
    # Cart -> CartItem relationship
    mapper_registry.map_imperatively(
        Cart,
        carts_table,
        properties={
            "items": relationship(
                CartItem, back_populates="cart", cascade="all, delete-orphan"
            ),
        },
    )

    # CartItem -> Cart relationship
    mapper_registry.map_imperatively(
        CartItem,
        cart_items_table,
        properties={"cart": relationship(Cart, back_populates="items")},
    )
