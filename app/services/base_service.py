from app.models.users_model import UsersModel
from http import HTTPStatus
import sqlalchemy.exc as e



class BaseService:
    
    def __init__(self, current_user_id, current_app) -> None:
        current_user = UsersModel.query.get_or_404(current_user_id, description='Current user does not exist!')
        self.current_user = current_user
        self.session = current_app.db.session

    def add_to_database(self, model: object):
        try:
            self.session.add(model)
            self.session.commit()
        except e.IntegrityError as ie:
            return str(ie.__dict__['orig']), HTTPStatus.UNPROCESSABLE_ENTITY

    def delete_from_database(self, model: object):
        try:
            self.session.delete(model)
            self.session.commit()
        except e.IntegrityError as ie:
            return str(ie.__dict__['orig']), HTTPStatus.UNPROCESSABLE_ENTITY