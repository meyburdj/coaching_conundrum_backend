import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
cors = CORS()

def create_app(config=None, script_info=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    if config:
        app.config.from_object(config)
    else:
        app_settings = os.getenv("APP_SETTINGS")
        app.config.from_object(app_settings)

        database_url = os.getenv('DATABASE_URL')
        if database_url is not None and database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    # Register API
    from src.api import api
    api.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
