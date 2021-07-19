from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api


def init_app(app: Flask):
    api = Api(app)
    JWTManager(app)

    from app.views import Notices

    api.add_resource(Notices, "/notices", endpoint="/notices", methods=["GET", "POST"])
    api.add_resource(
        Notices,
        "/notices/<notice_id>",
        endpoint="/notices/<notice_id>",
        methods=["GET", "DELETE", "PATCH"],
    )

    from app.views import Login

    api.add_resource(Login, "/login", endpoint="/login", methods=["POST"])

    from app.views import Users

    api.add_resource(Users, "/signup", endpoint="/signup", methods=["POST"])
    api.add_resource(Users, "/users", endpoint="/users", methods=["GET"])
    api.add_resource(
        Users,
        "/users/<user_id>",
        endpoint="/users/<user_id>",
        methods=["GET", "DELETE", "PATCH"],
    )

    from app.views import Polls

    api.add_resource(Polls, "/polls", endpoint="/poll", methods=["POST"])
    api.add_resource(Polls, "/polls", endpoint="/polls", methods=["GET"])
    api.add_resource(
        Polls, "/polls/<poll_id>", endpoint="/polls/<poll_id>", methods=["GET"]
    )

    from app.views import Events
    api.add_resource(Events, "/events", endpoint="/events", methods=['POST', 'GET'])
    api.add_resource(Events, "/events/<int:event_id>", endpoint="/events/<int:event_id>", methods=['PATCH', 'DELETE'])

    from app.views import Invitations
    api.add_resource(Invitations, "/invitations/<int:invitation_id>", endpoint="/invitations/<int:invitation_id>", methods=['PATCH', 'DELETE'])
    