from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.polls_votes_model import PollVoteSchema, PollsVotesModel
from app.models.users_model import UsersModel
from app.models.poll_options_model import PollOptionsModel
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e

class PollsVotes(Resource):
    def get(self, poll_votes_id=None):
        if poll_votes_id is None:
            polls_votes = PollsVotesModel().query.all()
            polls_votes_schema = PollVoteSchema()
            return {
                "polls_votes": polls_votes_schema.dump([polls_votes])
            }, HTTPStatus.OK
        
        else:
            try:
                poll_vote = PollsVotesModel.query.get_or_404(poll_votes_id)
                poll_vote_schema = PollVoteSchema
                return poll_vote_schema.dump(poll_vote)

            except e.DataError:
                return {
                    "message": "invalid number, just accept int with polls votes ids",
                    "error": "DataError"
                }, HTTPStatus.BAD_REQUEST

    
    def post(self, current_user: UsersModel, poll_option: PollOptionsModel):
        session = 
        poll_vote = PollsVotes()
        








