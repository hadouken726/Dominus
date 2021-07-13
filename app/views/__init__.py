from flask import Flask

from app.views.notices_view import bp as bp_notices
from app.views.test_view import bp as bp_test
from app.views.users_view import bp as bp_users


def init_app(app: Flask) -> None:
    app.register_blueprint(bp_test)
    app.register_blueprint(bp_notices)
    app.register_blueprint(bp_users)

