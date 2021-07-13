from .notices_view import Notices
from flask import Flask
from .test_view import Test
from app.views.users_view import bp as bp_users
def init_app(app: Flask):
    app.register_blueprint(bp_users)