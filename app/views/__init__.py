from flask import Flask
from app.views.test_view import bp as bp_test


def init_app(app: Flask):
    app.register_blueprint(bp_test)