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

    def get(self):
        pass

    def patch(self, event_id):
        request_data = request.get_json()
        events_service = EventsService(3)
        response = events_service.patch(event_id, request_data)
        return response

    def delete(self):
        pass
    