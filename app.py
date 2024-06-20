from flask import Flask
from src.database import db
from src.database.models import Base
from src.routes.endpoints import bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix='/api')
    Base.metadata.create_all(bind=db.engine)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
