from flask import Flask
from app import settings
from app.settings import database, migration, commands, api
from app import views


def create_app() -> Flask:
    app = Flask(__name__)
    settings.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    api.init_app(app)
    commands.init_app(app)
    return app