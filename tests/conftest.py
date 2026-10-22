import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app

from app.database.database import Base, get_db

# Import all models so SQLAlchemy knows about every table
from app.models.user import User
from app.models.client import Client
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction


TEST_DATABASE_URL = (
    "postgresql+psycopg2://harinathrayala"
    "@localhost:5432/wealthflow_test"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    # Clean all data before every test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(
    app,
    raise_server_exceptions=False
) as test_client:
        yield test_client

    app.dependency_overrides.clear()