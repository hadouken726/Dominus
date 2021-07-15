from .notices_view import Notices
from users_view import bp as bp_users
from flask import Flask, Blueprint


def init_app(app: Flask):
    bp_users