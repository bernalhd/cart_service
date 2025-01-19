from cart_service.app.domain.services.cart_service import (
    CartServiceImplementation,
)
from cart_service.app.infrastructure.grpc.proto.cart_service_pb2 import (
    AddToCartRequest,
    AddToCartResponse,
    CreateCartRequest,
    CreateCartResponse,
    GetCartRequest,
    GetCartResponse,
    RemoveFromCartRequest,
    RemoveFromCartResponse,
)
from cart_service.app.infrastructure.repository.sqlalchemy import (
    SqlAlchemyCartRepository,
)


class TestCartService:
    def test_create_cart_service(self, session):
        repo = SqlAlchemyCartRepository(session)
        service = CartServiceImplementation(repo)

        request = CreateCartRequest(user_id=1)
        response = service.CreateCart(request, None)

        assert isinstance(response, CreateCartResponse)
        assert response.cart_id is not None
        cart = repo.get_cart(response.cart_id)
        assert cart.user_id == 1

    def test_add_to_cart_service(self, session):
        repo = SqlAlchemyCartRepository(session)
        service = CartServiceImplementation(repo)

        request = CreateCartRequest(user_id=1)
        response = service.CreateCart(request, None)

        request = AddToCartRequest(
            cart_id=response.cart_id, product_id=1, quantity=1, unit_price=1.0
        )
        response = service.AddToCart(request, None)

        assert isinstance(response, AddToCartResponse)
        assert response.success
        cart = repo.get_cart(request.cart_id)
        assert len(cart.items) == 1
        assert cart.items[0].product_id == 1
        assert cart.items[0].quantity == 1
        assert cart.items[0].unit_price == 1.0

    def test_remove_from_cart_service(self, session):
        repo = SqlAlchemyCartRepository(session)
        service = CartServiceImplementation(repo)

        request = CreateCartRequest(user_id=1)
        response = service.CreateCart(request, None)
        cart_id = response.cart_id

        request = AddToCartRequest(
            cart_id=cart_id, product_id=1, quantity=1, unit_price=1.0
        )
        response = service.AddToCart(request, None)

        request = AddToCartRequest(
            cart_id=cart_id, product_id=2, quantity=2, unit_price=2.0
        )
        response = service.AddToCart(request, None)

        cart = repo.get_cart(cart_id)
        assert len(cart.items) == 2

        request = RemoveFromCartRequest(cart_id=cart_id, product_id=1)
        response = service.RemoveFromCart(request, None)

        assert isinstance(response, RemoveFromCartResponse)
        assert response.success
        assert len(cart.items) == 1
        assert cart.items[0].product_id == 2
        assert cart.items[0].quantity == 2
        assert cart.items[0].unit_price == 2.0

    def test_get_cart_service(self, session):
        repo = SqlAlchemyCartRepository(session)
        service = CartServiceImplementation(repo)

        request = CreateCartRequest(user_id=1)
        response = service.CreateCart(request, None)
        cart_id = response.cart_id

        request = AddToCartRequest(
            cart_id=cart_id, product_id=1, quantity=1, unit_price=1.0
        )
        response = service.AddToCart(request, None)

        request = AddToCartRequest(
            cart_id=cart_id, product_id=2, quantity=2, unit_price=2.0
        )
        response = service.AddToCart(request, None)

        request = AddToCartRequest(
            cart_id=cart_id, product_id=3, quantity=1, unit_price=3.0
        )
        response = service.AddToCart(request, None)

        cart = repo.get_cart(cart_id)
        assert len(cart.items) == 3

        request = GetCartRequest(cart_id=cart_id)
        response = service.GetCart(request, None)

        assert isinstance(response, GetCartResponse)
        assert response.cart.user_id == 1
        assert len(response.items) == 3
        assert response.total == 1.0 + 2.0 * 2 + 3.0
