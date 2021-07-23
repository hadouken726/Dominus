from operator import ne
from app.models.events_model import EventsModel
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
from app.services.base_service import BaseService

class InvitationsService(BaseService):

    
    def __init__(self, current_user_id, current_app) -> None:
        super().__init__(current_user_id, current_app)

    def get_all(self):
        invitations_received = list(EventsInvitationsModel.query.filter_by(guest_id=self.current_user.id))
        hosted_events = EventsModel.query.filter_by(host_id=self.current_user.id)
        invitations_sended = []
        for he in hosted_events:
            invitations_sended.extend(he.sended_invitations) 
        all_invitations = invitations_received + invitations_sended
        return EventInvitationSchema().dump(all_invitations, many=True), HTTPStatus.OK


    def get_one(self, invitation_id):
        invitation = EventsInvitationsModel.query.get_or_404(invitation_id)
        if invitation.guest_id == self.current_user.id or invitation.event.host_id == self.current_user.id:
            return EventInvitationSchema().dump(invitation), HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message='User is not in the event!')

    def patch(self, invitation_id):
        invitation = EventsInvitationsModel.query.get(invitation_id)
        if self.current_user.id == invitation.guest_id:
            try:
                updated_invitation = EventInvitationSchema(only=['status']).load(request.get_json(), session=self.session, instance=invitation, partial=True)
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
            self.add_to_database(updated_invitation)
            return EventInvitationSchema().dump(updated_invitation), 200
        abort(HTTPStatus.UNAUTHORIZED, message='Only guest can edit the invitation status')

    def delete(self, invitation_id):
        invitation_to_delete = EventsInvitationsModel.query.get(invitation_id)
        if invitation_to_delete.event.host_id == self.current_user.id:
            self.delete_from_database(invitation_to_delete)
            return '', HTTPStatus.NO_CONTENT
        abort(HTTPStatus.UNAUTHORIZED, message='Only event host can delete a invitation')

    def post(self, request_data):
        try:
            new_invite = EventInvitationSchema(exclude=['status']).load(request_data, session=self.session)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
        event = EventsModel.query.get_or_404(new_invite.event_id, description={'message': 'Event not found!'})
        user_to_invite = UsersModel.query.get_or_404(new_invite.guest_id, description={'message': 'User not found!'})
        if self.current_user.id != event.host_id:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='User is not host of the event!')
        if user_to_invite.id == self.current_user.id:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message="User can't invite himself")
        if EventsInvitationsModel.query.filter(EventsInvitationsModel.event_id == event.id, EventsInvitationsModel.guest_id == user_to_invite.id).first():
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='Invitation already exists!')
        self.add_to_database(new_invite)
        return EventInvitationSchema().dump(new_invite)
        
        
