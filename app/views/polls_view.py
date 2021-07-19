from flask.json import load
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.polls_model import PollsModel, PollSchema
from marshmallow import pre_load
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e
import json

from app.settings.database import db


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


    def post(self):
        session = current_app.db.session
        data = request.get_json()
        poll_schema = PollSchema()
        new_poll = poll_schema.load(data, session=session)

        session.add(new_poll)
        session.commit()

        return poll_schema.dump(new_poll)
