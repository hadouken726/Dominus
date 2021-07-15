from flask import Flask
from flask_restful import Api


def init_app(app: Flask):
    api = Api(app)
    
    from app.views import Notices
    api.add_resource(Notices, "/notices", endpoint="/notices", methods=["GET"])
    api.add_resource(Notices, "/notices/<notice_id>", endpoint="/notices/<int:notice_id>", methods=["GET"])
    api.add_resource(Notices, "/notices", endpoint="post_notice", methods=['POST'])


    from app.views import Test
    api.add_resource(Test, "/test", endpoint="/test", methods=["GET"])


    from app.views import Login
    api.add_resource(Login, "/login", endpoint="/login", methods=["POST"])


    from app.views import Users
    api.add_resource(Users, "/users", endpoint="signup", methods=["POST"])
