from app.models.users_model import UsersModel
from flask_restful import Resource
from app.services.events_service import EventsService
from flask import request

class Events(Resource):
    def post(self):
        request_data = request.get_json()
        events_service = EventsService(3)
        response = events_service.post(request_data)
        return response

    def get(self, event_id=None):
        if event_id is None:
            return EventsService(3).get_all()
        return EventsService(3).get(event_id)

    def patch(self, event_id):
        request_data = request.get_json()
        events_service = EventsService(3)
        response = events_service.patch(event_id, request_data)
        return response

    def delete(self, event_id):
        events_service = EventsService(3)
        response = events_service.delete(event_id)
        return response
    