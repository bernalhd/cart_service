import cart_service.app.infrastructure.grpc.proto.cart_service_pb2 as cart_service_pb2
import cart_service.app.infrastructure.grpc.proto.cart_service_pb2_grpc as cart_service_pb2_grpc
from cart_service.app.domain.ports.repository import CartRepository


class CartServiceImplementation(cart_service_pb2_grpc.CartServiceServicer):
    def __init__(self, cart_repository: CartRepository):
        self.cart_repository = cart_repository

    def CreateCart(
        self, request: cart_service_pb2.CreateCartRequest, context
    ) -> cart_service_pb2.CreateCartResponse:
        cart = self.cart_repository.create_cart(request.user_id)
        return cart_service_pb2.CreateCartResponse(cart_id=cart.id)

    def RemoveCart(
        self, request: cart_service_pb2.RemoveCartRequest, context
    ) -> cart_service_pb2.RemoveCartResponse:
        removed_cart = self.cart_repository.remove_cart(
            cart_id=request.cart_id
        )
        return cart_service_pb2.RemoveCartResponse(success=removed_cart)

    def AddToCart(
        self, request: cart_service_pb2.AddToCartRequest, context
    ) -> cart_service_pb2.AddToCartResponse:
        success = self.cart_repository.add_item_to_cart(
            request.cart_id,
            request.product_id,
            request.quantity,
            request.unit_price,
        )
        return cart_service_pb2.AddToCartResponse(success=success)

    def RemoveFromCart(
        self, request: cart_service_pb2.RemoveFromCartRequest, context
    ) -> cart_service_pb2.RemoveFromCartResponse:
        success = self.cart_repository.remove_item_from_cart(
            request.cart_id, request.product_id
        )
        return cart_service_pb2.RemoveFromCartResponse(success=success)

    def GetCart(
        self, request: cart_service_pb2.GetCartRequest, context
    ) -> cart_service_pb2.GetCartResponse:
        cart = self.cart_repository.get_cart(request.cart_id)
        total = sum([item.quantity * item.unit_price for item in cart.items])
        response = cart_service_pb2.GetCartResponse(
            cart=cart_service_pb2.Cart(id=cart.id, user_id=cart.user_id),
            items=[
                cart_service_pb2.CartItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in cart.items
            ],
            total=total,
        )

        return response
