from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.polls_votes_model import PollVoteSchema, PollsVotesModel
from app.models.poll_options_model import PollOptionsModel
from app.models.polls_model import PollsModel
from app.models.users_model import UsersModel
from http import HTTPStatus
from flask_restful import Resource, abort
import sqlalchemy.exc as e
import ipdb


class PollsVotes(Resource):
    def get(self, poll_votes_id=None):
        if poll_votes_id is None:
            polls_votes = PollsVotesModel().query.all()
            polls_votes_schema = PollVoteSchema()

            return {
                "polls_votes": polls_votes_schema.dump(polls_votes, many=True)
            }, HTTPStatus.OK

        else:
            try:
                poll_vote = PollsVotesModel.query.get_or_404(poll_votes_id)
                poll_vote_schema = PollVoteSchema
                return poll_vote_schema.dump(poll_vote)

            except e.DataError:
                return {
                    "message": "invalid number, just accept int with polls votes ids",
                    "error": "DataError",
                }, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        session = current_app.db.session
        data = request.get_json()
        current_user_id = get_jwt_identity()
        current_user = UsersModel().query.get_or_404(current_user_id, description='User not found!')
        poll_vote = PollVoteSchema().load(data, session=session)
        if PollsVotesModel.query.filter(PollsVotesModel.owner_id == current_user_id, PollsVotesModel.option.poll_id == poll_vote.option.poll_id).first():
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='User already vote in this poll!')     
        session.add(poll_vote)
        session.commit()

        option = poll_vote.option

        return {
            "vote": {
                "user_name": current_user.name,
                "poll": PollsModel().query.get(option.poll_id).title,
                "poll_option": option.name,
            }
        }
