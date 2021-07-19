from flask.json import jsonify, load
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.polls_model import PollsModel
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
            return {"msg": polls.title}

        else:
            poll: PollsModel = PollsModel().query.get(poll_id)
            return {"title": poll.title}

    def post(self):
        session = current_app.db.session
        data = request.get_json()
        new_poll: PollsModel = PollsModel(**data)

        session.add(new_poll)
        session.commit()

        return {"msg": new_poll.title}
