from flask import Flask

from app.views.notices_view import bp as bp_notices
from app.views.test_view import bp as bp_test



def init_app(app: Flask):
    app.register_blueprint(bp_test)
    app.register_blueprint(bp_notices)