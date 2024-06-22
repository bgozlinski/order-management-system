import pytest
from src.app import create_app
from src.database.db import get_engine, SessionLocal
from src.database.models import Base


@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    app.config.update({
        "TESTING": True,
    })

    engine = get_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    SessionLocal.configure(bind=engine)

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    yield app

    with app.app_context():
        Base.metadata.drop_all(bind=engine)
        SessionLocal.remove()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def session(app, request):
    connection = SessionLocal().bind.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    db_session = SessionLocal(**options)

    def cleanup():
        transaction.rollback()
        connection.close()
        db_session.close()

    request.addfinalizer(cleanup)
    return db_session
