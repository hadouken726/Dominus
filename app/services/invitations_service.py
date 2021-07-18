from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import request, current_app
from flask_restful import abort
from app.models.users_model import UsersModel
from app.models.events_invitations_model import EventsInvitationsModel, EventInvitationSchema 
from marshmallow import ValidationError


class InvitationsService:

    
    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get(current_user_id)
        if fetched_user:
            self.current_user = fetched_user
            self.session = current_app.db.session
        else:
            abort(HTTPStatus.BAD_REQUEST, message='Invalid user!')
    
    def _deserialize(self, invitation_data: dict):
        try:
            return EventInvitationSchema().load(invitation_data, session=self.session)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
        
