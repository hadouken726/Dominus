from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api


def init_app(app: Flask):
    api = Api(app)
    JWTManager(app)

    from app.views import Notices
    api.add_resource(Notices, "/notices", endpoint="/notices", methods=["GET", "POST"])
    api.add_resource(Notices, "/notices/<notice_id>", endpoint="/notices", methods=["GET", "DELETE", "PATCH"])


    from app.views import Login
    api.add_resource(Login, "/login", endpoint="/login", methods=["POST"])


    from app.views import Users
    api.add_resource(Users, "/signup", endpoint="/users", methods=["POST"])
    api.add_resource(Users, "/users", endpoint="/users", methods=["GET"])
    api.add_resource(Users, "/users/<user_id>", endpoint="/users", methods=["GET", "DELETE", "PATCH"])