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


class InvitationsService:

    
    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get(current_user_id)
        if fetched_user:
            self.current_user = fetched_user
            self.session = current_app.db.session
        else:
            abort(HTTPStatus.BAD_REQUEST, message='Invalid user!')

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
        if EventsInvitationsModel.query.filter(EventsInvitationsModel.event_id == event.id, EventsInvitationsModel.guest_id == user_to_invite.id):
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='Invitation already exists!')
        self.session.add(new_invite)
        self.session.commit()
        return EventInvitationSchema().dump(new_invite)
        
        
