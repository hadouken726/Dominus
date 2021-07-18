from functools import partial
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import request, current_app
from flask_restful import abort
from marshmallow.utils import pprint
from sqlalchemy.util.langhelpers import only_once
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

    def get(self):
        pass

    def patch(self, invitation_id):
        invitation = EventsInvitationsModel.query.get(invitation_id)
        if self.current_user.id == invitation.guest_id:
            try:
                updated_invitation = EventInvitationSchema(only=['status']).load(request.get_json(), session=self.session, instance=invitation, partial=True)
                self.session.add(updated_invitation)
                self.session.commit()
                return EventInvitationSchema().dump(updated_invitation), 200
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
        abort(HTTPStatus.UNAUTHORIZED, message='Only guest can edit the invitation status')

    def delete(self, invitation_id):
        invitation_to_delete = EventsInvitationsModel.query.get(invitation_id)
        if invitation_to_delete.event.host_id == self.current_user.id:
            self.session.delete(invitation_to_delete)
            self.session.commit()
            return '', HTTPStatus.NO_CONTENT
        abort(HTTPStatus.UNAUTHORIZED, message='Only event host can delete a invitation')
        
