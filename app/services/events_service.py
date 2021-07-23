import sqlalchemy.exc as e
from app.models.events_invitations_model import EventInvitationSchema, EventsInvitationsModel
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import current_app, request
from flask_restful import abort
from app.models.users_model import UsersModel
from app.models.events_model import EventsModel, EventSchema
from marshmallow import ValidationError
from typing import List
from marshmallow import Schema, fields
from app.services.base_service import BaseService



class EventsService(BaseService):

    
    def __init__(self, current_user_id, current_app) -> None:
        super().__init__(current_user_id, current_app)


    def _deserialize(self, request_data: dict):
        try:
            return EventSchema().load(request_data, session=self.session)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, message=VE.messages)

        
    def _get_all_other_users(self):
        all_users = UsersModel.query.all()
        all_users.remove(self.current_user)
        return all_users

    def _admin_post(self, new_event: EventsModel):
        all_other = self._get_all_other_users()
        self.send_invitation(all_other, new_event)

    def send_invitation(self, users: List[UsersModel], event: EventsModel):
        for user in users:
            invitation = EventInvitationSchema().load({"event_id": event.id, "guest_id": user.id}, session=self.session)
            event.sended_invitations.append(invitation)
        self.session.add(event)
        self.session.commit()

    def post(self, requested_data: dict):
        new_event = self._deserialize(requested_data)
        new_event.host_id = self.current_user.id
        if new_event.is_important:
            if self.current_user.is_admin:
                self._admin_post(new_event)
            else:
                abort(HTTPStatus.UNAUTHORIZED, message='Only admin users can create important events!')
        else:
            self.add_to_database(new_event)
        return EventSchema().dump(new_event), HTTPStatus.CREATED

    def patch(self, event_id: int, request_data: dict):
        event = EventsModel.query.get(event_id)
        if not event:
            abort(HTTPStatus.NOT_FOUND, message='Event not found')
        if event.host_id == self.current_user.id or self.current_user.is_admin:
            updated_event = EventSchema().load(request_data, instance=event, partial=True, session=self.session)
            self.add_to_database(updated_event)
            return EventSchema().dump(updated_event), HTTPStatus.OK
        else:
            abort(HTTPStatus.UNAUTHORIZED, message='Only event host or admin users can edit the event!')
        
    def delete(self, event_id: int):
        event_to_delete = EventsModel().query.get(event_id)
        if not event_to_delete:
            abort(HTTPStatus.NOT_FOUND, message='Event not found')
        if self.current_user.is_admin or event_to_delete.host_id == self.current_user.id:
            self.delete_from_database(event_to_delete)
            return '', HTTPStatus.NO_CONTENT
        
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin user or event host can delete this event')

    def get_all(self):
        all_events = EventsModel.query.all()
        events_hosted_by_current_user = list(EventsModel.query.filter_by(host_id=self.current_user.id))
        accepted_invitations = EventsInvitationsModel.query.filter(EventsInvitationsModel.guest_id == self.current_user.id, EventsInvitationsModel.status == 'accepted')
        events_in = [invitation.event for invitation in accepted_invitations]
        if self.current_user.is_admin:
            return EventSchema().dump(all_events, many=True)
        return EventSchema().dump(events_hosted_by_current_user + events_in, many=True)
    
    def get(self, event_id):
        event = EventsModel.query.get(event_id)
        current_user_invitations_received = EventsInvitationsModel.query.filter_by(guest_id=self.current_user.id)
        is_current_user_invited = False
        if any([event.id == ri.event_id for ri in current_user_invitations_received]):
            is_current_user_invited = True

        if not event:
            abort(HTTPStatus.NOT_FOUND, message='Event not found')
        if self.current_user.id == event.host_id or self.current_user.is_admin or is_current_user_invited:
            return EventSchema().dump(event), HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message="Current user can't access this event")



        
        
