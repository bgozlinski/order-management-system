from flask import Flask

from src.database.db import get_engine
from src.database.models import Base
from src.routes.endpoints import bp
import os


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///:memory:'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    engine = get_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    Base.metadata.create_all(bind=engine)

    app.register_blueprint(bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
