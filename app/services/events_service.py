from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask_restful import abort
from app.models.users_model import UsersModel
from app.models.events_model import EventsModel, EventSchema
from marshmallow import ValidationError



class EventsServices:


    def get_request(self, request_data: dict):
        event_schema = EventSchema()
        try:
            new_event = event_schema.load(request_data)
            return event_schema.dump(new_event)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, messages=VE.messages)
    
    
        
