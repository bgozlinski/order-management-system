import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from src.database.db import engine, SessionLocal, get_engine
from src.database.models import Base


@pytest.fixture(scope='session')
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    engine = app.engine

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield app
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    connection = app.engine.connect()  # Use app.engine which is configured for testing
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = SessionLocal(**options)

    # Ensure the session is used for the app context
    app.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.close()

    # Clean up the database between tests
    Base.metadata.drop_all(bind=app.engine)
    Base.metadata.create_all(bind=app.engine)
