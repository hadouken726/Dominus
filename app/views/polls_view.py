from flask import request, current_app
from flask.json import load
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from marshmallow import pre_load
from http import HTTPStatus
import sqlalchemy.exc as e

from app.models.polls_model import PollsModel, PollSchema
from app.models.users_model import UsersModel

class Polls(Resource):
    def get(self, poll_id=None):
        if poll_id is None:
            polls: PollsModel = PollsModel().query.all()
            polls_schema = PollSchema()
            return {"polls": polls_schema.dump(polls, many=True)}, HTTPStatus.OK

        else:
            try:
                poll: PollsModel = PollsModel().query.get_or_404(poll_id)
                polls_schema = PollSchema()
                return polls_schema.dump(poll), HTTPStatus.OK

            except e.DataError:
                return {
                    "message": "invalid number, just accept int with register ids",
                        "error": "DataError"
                }, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = UsersModel().query.get(current_user_id)
        if current_user.is_admin:
            try:
                session = current_app.db.session
                data = request.get_json()
                poll_schema = PollSchema()
                new_poll = poll_schema.load(data, session=session)

                session.add(new_poll)
                session.commit()

                return poll_schema.dump(new_poll)
            
            except ValidationError as VE:
                return VE.messages
        if not current_user_id:
            return {"message": "user don't have admin permission to create a new notice"}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def delete(self, poll_id=None):
        current_user_id = get_jwt_identity()
        current_user = UsersModel().query.get(current_user_id)
        if current_user.is_admin:
            session = current_app.db.session
            poll = PollsModel.query.get_or_404(poll_id)

            session.delete(poll)
            session.commit()

            return {
                "message": f"Poll {poll.id} has been deleted"
            }
        
        if not current_user.is_admin:
            return {
                "message": "user don't have admin permission to delete polls"
            }, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def patch(self, poll_id=None):
        try:
            session = current_app.db.session
            data = request.get_json()
            poll = PollsModel.query.get_or_404(poll_id)
            new_poll = PollSchema().load(data, partial=True, session=session, instance=poll)
            session.add(new_poll)
            session.commit()

            return PollSchema().dump(new_poll)

        except ValidationError as VE:
            return VE.messages