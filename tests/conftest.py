import pytest
from src.app import create_app
from src.database.models import Base
from src.database.db import get_engine, SessionLocal


@pytest.fixture(scope='session')
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        Base.metadata.create_all(bind=get_engine())
        yield app
        Base.metadata.drop_all(bind=get_engine())


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def session(app):
    connection = get_engine().connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = SessionLocal(**options)

    app.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.close()
