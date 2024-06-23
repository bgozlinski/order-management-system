"""
This script initializes and runs the Flask application.

It loads environment variables from a .env file, creates the Flask application
instance with the specified configuration, and runs the development server.

Functions:
    create_app(config_name): Factory function to create a Flask application instance.

Environment Variables:
    FLASK_CONFIG: The configuration name to be used for the Flask application.

Usage:
    To run the Flask application, execute this script. Ensure that the .env file contains
    the necessary environment variables, including FLASK_CONFIG.
"""

from dotenv import load_dotenv
from src.app import create_app
import os
load_dotenv()

app = create_app(os.environ.get('FLASK_CONFIG'))

if __name__ == '__main__':
    app.run()
