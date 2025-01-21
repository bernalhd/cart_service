import grpc
import cart_service.app.infrastructure.grpc.proto.cart_service_pb2 as cart_service_pb2
import cart_service.app.infrastructure.grpc.proto.cart_service_pb2_grpc as cart_service_pb2_grpc

channel = grpc.insecure_channel("db:50051")

stub = cart_service_pb2_grpc.CartServiceStub(channel)

number = cart_service_pb2.CreateCartRequest(user_id=1)

response = stub.CreateCart(number)

print(response.cart_id)
