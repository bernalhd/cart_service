import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from cart_service.app.infrastructure.db_config import db_config
from cart_service.app.infrastructure.repository.orm import start_mappers
from cart_service.app.infrastructure.repository.sqlalchemy import (
    SqlAlchemyCartRepository,
)


metadata = db_config.get_metadata()


@pytest.fixture
def cart_repository(session):
    return SqlAlchemyCartRepository(session)


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    Session = sessionmaker(bind=in_memory_db)
    session = Session()
    yield session
    clear_mappers()
    session.close()
