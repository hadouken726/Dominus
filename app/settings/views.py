from flask import Flask
from flask_restful import Api


def init_app(app: Flask):
    api = Api(app)
    from app.views import Notices, Test, Users
    api.add_resource(Notices, "/notices", endpoint="/notices", methods=["GET"])
    api.add_resource(Notices, "/notices/<notice_id>", endpoint="/notices/<int:notice_id>", methods=["GET"])
    api.add_resource(Test, "/test", endpoint="/test", methods=["GET"])
    api.add_resource(Users, "/users", endpoint="/users", methods=["POST"])
    api.add_resource(Users, "/users", endpoint="/users", methods=["GET"])
    api.add_resource(Users, "/users/<user_id>", endpoint="/users/<user_id>", methods=["GET"])
    api.add_resource(Users, "/users/<user_id>", endpoint="/users/<user_id>", methods=["DELETE"])
    api.add_resource(Users, "/users/<user_id>", endpoint="/users/<user_id>", methods=["PATCH"])


