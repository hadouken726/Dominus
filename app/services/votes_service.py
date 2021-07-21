from app.views.poll_options_view import PollOptions
from http import HTTPStatus
from flask import request, current_app
from flask_restful import abort

from app.models.users_model import UsersModel
from app.models.polls_votes_model import PollsVotesModel
from app.models.poll_options_model import PollOptionsModel

class InvitationService:

    def __init__(self, current_polls_votes_id) -> None:
        fetched_poll_vote = UsersModel.query.get(current_polls_votes_id)
        if fetched_poll_vote:
            self.current_poll_vote = fetched_poll_vote
            self.session = current_app.db.session
        else:
            abort(HTTPStatus.BAD_REQUEST, message="Invalid user!")
    

    def get_all(self):
        voter = list(PollsVotesModel.query.filter_by(owner_id=self.current_user.id))
        option_chosen = list(PollOptionsModel.query.filter_by(option_id=))


    