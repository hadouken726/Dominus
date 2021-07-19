from flask.json import load
from flask import request, current_app
from sqlalchemy.orm import session
from app.models.poll_options_model import PollOptionsModel, PollOptionSchema
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e

from app.settings.database import db

class PollOptions(Resource):
    def get(self, poll_option_id=None):
        if poll_option_id is None:
            poll_options: PollOptionsModel = PollOptionsModel().query.all()
            poll_options_schema = PollOptionSchema()
            return {
                "poll_options": poll_options_schema.dump(poll_options, many=True)
            }, HTTPStatus.OK

        else:
            try: 
                poll_option: PollOptionsModel = PollOptionsModel.query.get_or_404(poll_option_id)
                poll_option_schema = PollOptionSchema()
                return poll_option_schema.dump(poll_option), HTTPStatus.OK

            except e.DataError:
                return {
                     "message": "invalid number, just accept int with register ids",
                        "error": "DataError"
                }, HTTPStatus.BAD_REQUEST


    def post(self):
        session = current_app.db.session
        data = request.get_json()
        poll_option_schema = PollOptionSchema()
        new_poll_option = poll_option_schema.load(data, session=session)

        session.add(new_poll_option)
        session.commit()

        return poll_option_schema.dump(new_poll_option)