import pytest
from app import create_app
from src.database.db import engine, SessionLocal
from src.database.models import Base


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        Base.metadata.create_all(bind=engine)
        yield app
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    connection = engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = SessionLocal(**options)

    app.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.close()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
