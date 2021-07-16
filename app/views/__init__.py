from .notices_view import Notices
from users_view import bp as bp_users
from flask import Flask, Blueprint


def init_app(app: Flask):

    from app.views.login_view import Login
    from app.views.notices_view import Notices
    from app.views.test_view import Test
    from app.views.users_view import Users

from app.views.test_view import Test
from app.views.users_view import Users