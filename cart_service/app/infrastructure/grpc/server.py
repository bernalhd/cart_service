from concurrent import futures

import cart_service.app.infrastructure.grpc.proto.cart_service_pb2_grpc as cart_service_pb2_grpc
import grpc
from cart_service.app.domain.services.cart_service import (
    CartServiceImplementation,
)
from cart_service.app.infrastructure.db_config import db_config
from cart_service.app.infrastructure.repository.orm import start_mappers
from cart_service.app.infrastructure.repository.sqlalchemy import (
    SqlAlchemyCartRepository,
)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    start_mappers()
    db_config.init_db()
    cart_repository = SqlAlchemyCartRepository(session=db_config.get_session())
    cart_service_pb2_grpc.add_CartServiceServicer_to_server(
        CartServiceImplementation(cart_repository=cart_repository), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
