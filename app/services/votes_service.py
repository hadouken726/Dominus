from flask import request, current_app
from app.models.users_model import UsersModel

class VotesServices:

    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get(current_user_id)
        if fetched_user:
            self.current_user = fetched_user
            self.session = current_app.db.session

    def get(self, vote_id=None):
        if vote_id is None:
            return 
        pass
    