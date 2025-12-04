from flask import Flask
from config import Config
from extensions import db, cors
from blueprints.reservations import reservations
from models import reservation  # ensure model is registered

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    # Register blueprints
    app.register_blueprint(reservations)

    return app
