from flask import Flask

from src.database.db import get_engine
from src.database.models import Base
from src.routes.endpoints import bp
import os


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        database_url = f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('DB_HOST_IP')}:5432/{os.getenv('POSTGRES_DB')}"
    else:
        database_url = test_config["SQLALCHEMY_DATABASE_URI"]

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    engine = get_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    app.engine = engine

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    app.register_blueprint(bp, url_prefix='/api')

    return app
