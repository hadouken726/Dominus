from flask import Flask
from app import settings
from app.settings import database, migration
from app import views


def create_app() -> Flask:
    app = Flask(__name__)
    settings.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    views.init_app(app)
    return app