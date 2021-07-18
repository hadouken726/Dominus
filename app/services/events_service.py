from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import current_user
from app.models.events_invitations_model import EventInvitationSchema
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from flask_restful import abort
from app.models.users_model import UsersModel
from app.models.events_model import EventsModel, EventSchema
from marshmallow import ValidationError, error_store
from typing import List



class EventsService:

    
    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get(current_user_id)
        if fetched_user:
            self.current_user = fetched_user
            self.session = current_app.db.session
        else:
            abort(HTTPStatus.BAD_REQUEST, message='Invalid user!')


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
        requested_data['host_id'] = self.current_user.id
        new_event = self._deserialize(requested_data)
        if new_event.is_important:
            if self.current_user.is_admin:
                self._admin_post(new_event)
            else:
                abort(HTTPStatus.UNAUTHORIZED, message='Only admin users can create important events!')
        else:
            self.session.add(new_event)
            self.session.commit()
        return EventSchema().dump(new_event), HTTPStatus.CREATED

    def patch(self, event_id: int, request_data: dict):
        event = EventsModel.query.get(event_id)
        if not event:
            abort(HTTPStatus.NOT_FOUND, message='Event not found')
        if event.host_id == self.current_user.id or self.current_user.is_admin:
            updated_event = EventSchema().load(request_data, instance=event, partial=True, session=self.session)
            self.session.add(updated_event)
            self.session.commit()
            return EventSchema().dump(updated_event), HTTPStatus.OK
        else:
            abort(HTTPStatus.UNAUTHORIZED, message='Only event host or admin users can edit the event!')
        


        
        
