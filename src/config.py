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
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:"
        f"{os.environ.get('POSTGRES_PASSWORD')}@"
        f"{os.environ.get('DB_HOST_IP')}:5432/{os.getenv('TEST_POSTGRES_DB')}"
    )
    TESTING = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
