import pytest
from src.app import create_app
from src.database.db import get_engine, SessionLocal, get_db
from src.database.models import Base
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='function')
def app():
    app = create_app('testing')

    return app


@pytest.fixture(scope='function')
def engine(app):
    """
    Returns session-wide initialized database engine.
    """
    engine = get_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    SessionLocal.configure(bind=engine)
    return engine


@pytest.fixture(scope='function')
def tables(engine):
    """
    Returns session-wide initialized database tables.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function')
def session(engine, tables, request):
    """
    Creates a new database session for a test.
    """
    connection = engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = SessionLocal(**options)

    def teardown():
        transaction.rollback()
        connection.close()
        session.close()

    request.addfinalizer(teardown)
    return session


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()
