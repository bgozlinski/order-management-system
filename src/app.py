from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config import config_by_name
from src.routes.endpoints import api_orders_bp

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name: str) -> Flask:
    """
    Factory function to create a Flask application instance.

    This function sets up the Flask application with the specified configuration, initializes
    the SQLAlchemy and Flask-Migrate extensions, and registers the application blueprints.

    Args:
        config_name (str): The configuration name to be used for the Flask application. This
                           should correspond to a key in the config_by_name dictionary.

    Returns:
        Flask: The initialized Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api_orders_bp)

    return app
