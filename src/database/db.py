"""
This module provides the SQLAlchemy database setup and utility functions for creating
and managing database sessions.

Functions:
    get_engine(database_url): Returns a SQLAlchemy engine instance.
    get_db(): Generator function that provides a database session for dependency injection.

Environment Variables:
    DATABASE_URL: The URL for the database connection.
    POSTGRES_USER: The PostgreSQL user.
    POSTGRES_PASSWORD: The PostgreSQL password.
    DB_HOST_IP: The IP address of the PostgreSQL host.
    POSTGRES_DB: The name of the PostgreSQL database.

Usage:
    Import this module to access the SQLAlchemy engine and session management functions.
"""

import sqlalchemy
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


def get_engine(database_url=None) -> sqlalchemy.engine:
    """
    Returns a SQLAlchemy engine instance.

    This function creates a new SQLAlchemy engine using the provided database URL.
    If no URL is provided, it defaults to the URL specified in the SQLALCHEMY_DATABASE_URL variable.

    Args:
        database_url (str, optional): The database URL to use for creating the engine. Defaults to None.

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine instance.
    """
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
