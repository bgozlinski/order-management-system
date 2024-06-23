"""
This module defines configuration classes for different environments and loads environment variables.

Classes:
    Config: Base configuration class with common settings.
    DevelopmentConfig: Configuration class for development environment with PostgreSQL database settings.
    TestingConfig: Configuration class for testing environment with SQLite in-memory database settings.

Variables:
    config_by_name (dict): A dictionary to map configuration names to their corresponding configuration classes.

Usage:
    Import this module to use the configuration settings in a Flask application.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}@"
        f"{os.environ.get('DB_HOST_IP')}:5432/{os.getenv('POSTGRES_DB')}"
    )


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
