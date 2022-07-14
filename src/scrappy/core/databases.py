from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from scrappy.core.settings import DEFAULT_DATABASE


class Database:
    def __init__(self, url):
        self.SQLALCHEMY_DATABASE_URL = url
        # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

        if "postgresql" in url:
            self.engine = create_engine(
                self.SQLALCHEMY_DATABASE_URL, pool_pre_ping=False
            )
        else:
            self.engine = create_engine(
                self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
            )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        self.Base = declarative_base()

    @contextmanager
    def manager_to_get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Dependency
    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


default = Database(
    # url="sqlite:///./sql_app.db"
    url=DEFAULT_DATABASE
)
