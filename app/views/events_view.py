import jwt
from app.models.users_model import UsersModel
from flask_restful import Resource
from app.services.events_service import EventsService
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

class Events(Resource):

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        request_data = request.get_json()
        events_service = EventsService(current_user_id)
        response = events_service.post(request_data)
        return response

    @jwt_required()
    def get(self, event_id=None):
        current_user_id = get_jwt_identity()
        events_service = EventsService(current_user_id)
        if event_id is None:
            return events_service.get_all()
        return events_service.get(event_id)

    @jwt_required()
    def patch(self, event_id):
        current_user_id = get_jwt_identity()
        events_service = EventsService(current_user_id)
        request_data = request.get_json()
        response = events_service.patch(event_id, request_data)
        return response

    @jwt_required()
    def delete(self, event_id):
        current_user_id = get_jwt_identity()
        events_service = EventsService(current_user_id)
        response = events_service.delete(event_id)
        return response
    