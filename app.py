from flask import Flask
from src.database import db

app = Flask(__name__)


def create_app():
    app = Flask(__name__)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
