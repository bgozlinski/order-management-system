from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f"postgresql+psycopg2://"
    f"{os.environ.get('POSTGRES_USER')}:"
    f"{os.environ.get('POSTGRES_PASSWORD')}@"
    f"{os.environ.get('DB_HOST_IP')}:5432/"
    f"{os.getenv('POSTGRES_DB')}")


def get_engine(database_url=None):
    if database_url is None:
        database_url = SQLALCHEMY_DATABASE_URL
    return create_engine(database_url)


engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generator function that provides a database session.

    This function is intended for use with dependency injection in web applications,
    ensuring that a new database session is created for each request and properly closed after use.

    Yields:
        SessionLocal: An instance of a SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
