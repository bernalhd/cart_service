import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import registry, sessionmaker

load_dotenv()


class DatabaseConfig:
    def __init__(self):
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://user:password@localhost:5432/mydatabase",
        )
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        self.metadata = MetaData()
        self.mapper_registry = registry()
        self.SessionFactory = sessionmaker(bind=self.engine)

    def get_engine(self):
        return self.engine

    def get_metadata(self):
        return self.metadata

    def get_mapper_registry(self):
        return self.mapper_registry

    def get_session(self):
        return self.SessionFactory()

    def init_db(self):
        self.metadata.create_all(self.engine)


db_config = DatabaseConfig()
