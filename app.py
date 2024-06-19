from flask import Flask
from src.database import db
from src.database.models import Base


def create_app():
    app = Flask(__name__)
    Base.metadata.create_all(bind=db.engine)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
