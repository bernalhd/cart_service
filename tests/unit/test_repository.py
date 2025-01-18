from sqlalchemy import text
import pytest
from cart_service.app.domain.models import CartAlreadyExistsError


class TestSqlAlchemyCartRepository:
    def _create_cart_in_db(self, session, user_id):
        session.execute(
            text("INSERT INTO carts (user_id) VALUES (:user_id)"),
            {"user_id": user_id},
        )
        session.commit()
        return (
            session.execute(
                text(
                    "SELECT id FROM carts WHERE user_id = :user_id ORDER BY id DESC LIMIT 1"
                ),
                {"user_id": user_id},
            )
            .mappings()
            .fetchone()["id"]
        )

    def _add_item_to_cart_in_db(
        self, session, user_id, product_id, quantity, unit_price
    ):
        cart_id = (
            session.execute(
                text("SELECT id FROM carts WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            .mappings()
            .fetchone()["id"]
        )
        session.execute(
            text(
                "INSERT INTO cart_items (cart_id, product_id, quantity, unit_price) VALUES (:cart_id, :product_id, :quantity, :unit_price)"
            ),
            {
                "cart_id": cart_id,
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
            },
        )
        session.commit()

    def _get_cart_items_from_db(self, session, user_id):
        cart_id = (
            session.execute(
                text("SELECT id FROM carts WHERE user_id = :user_id"),
                {"user_id": user_id},
            )
            .mappings()
            .fetchone()["id"]
        )
        return (
            session.execute(
                text("SELECT * FROM cart_items WHERE cart_id = :cart_id"),
                {"cart_id": cart_id},
            )
            .mappings()
            .fetchall()
        )

    def test_create_cart_success(self, session, cart_repository):
        user_id = 42
        cart = cart_repository.create_cart(user_id)

        assert cart.id is not None
        assert cart.user_id == user_id

        query = text("SELECT id, user_id FROM carts WHERE user_id = :user_id")
        result = (
            session.execute(query, {"user_id": user_id}).mappings().fetchone()
        )

        assert result is not None
        assert result["user_id"] == user_id

    def test_create_cart_failure_cart_exists(self, session, cart_repository):
        user_id = 42
        self._create_cart_in_db(session, user_id)
        with pytest.raises(CartAlreadyExistsError):
            cart_repository.create_cart(user_id)

    def test_remove_cart_success(self, session, cart_repository):
        user_id = 42
        self._create_cart_in_db(session, user_id)
        cart_repository.remove_cart(user_id)
        query = text("SELECT * FROM carts WHERE user_id = :user_id")
        result = session.execute(query, {"user_id": user_id}).fetchone()
        assert result is None

    def test_add_item_to_cart_success(self, session, cart_repository):
        user_id = 1
        self._create_cart_in_db(session, user_id)

        product_id = 101
        quantity = 2
        unit_price = 10.0

        success = cart_repository.add_item_to_cart(
            user_id, product_id, quantity, unit_price  # Ahora se pasa user_id
        )
        assert success is True

        result = self._get_cart_items_from_db(session, user_id)
        assert len(result) == 1
        assert result[0]["product_id"] == product_id
        assert result[0]["quantity"] == quantity
        assert result[0]["unit_price"] == unit_price

    def test_remove_item_from_cart_success(self, session, cart_repository):
        user_id = 1
        self._create_cart_in_db(session, user_id)

        product_id = 101
        quantity = 2
        unit_price = 10.0

        self._add_item_to_cart_in_db(
            session, user_id, product_id, quantity, unit_price
        )

        # Remove item from cart, if the quantity is greater than 1, the quantity should be reduced
        result = cart_repository.remove_item_from_cart(
            user_id=user_id, product_id=product_id
        )
        assert result is True

        items_in_cart = self._get_cart_items_from_db(session, user_id)
        assert len(items_in_cart) == 1
        assert items_in_cart[0]["quantity"] == 1

        # Remove item from cart, if the quantity is 1, the item should be removed
        result = cart_repository.remove_item_from_cart(
            user_id=user_id, product_id=product_id
        )
        assert result is True

        items_in_cart = self._get_cart_items_from_db(session, user_id)
        assert len(items_in_cart) == 0

    def test_get_cart_success(self, session, cart_repository):
        user_id = 1
        self._create_cart_in_db(session, user_id)

        product_id = 101
        quantity = 2
        unit_price = 10.0

        self._add_item_to_cart_in_db(
            session, user_id, product_id, quantity, unit_price
        )

        cart = cart_repository.get_cart(user_id)

        assert cart is not None
        assert cart.user_id == user_id
        assert len(cart.items) == 1
        assert cart.items[0].product_id == product_id
        assert cart.items[0].quantity == quantity
        assert cart.items[0].unit_price == unit_price

    def test_get_cart_items_success(self, session, cart_repository):
        user_id = 1
        self._create_cart_in_db(session, user_id)
        product_id = 101
        quantity = 2
        unit_price = 10.0

        self._add_item_to_cart_in_db(
            session, user_id, product_id, quantity, unit_price
        )

        items = cart_repository.get_cart_items(user_id)

        assert len(items) == 1
        assert items[0].product_id == product_id
        assert items[0].quantity == quantity
        assert items[0].unit_price == unit_price
