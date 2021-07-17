from flask_restful import Resource
from app.services.events_service import EventsServices
from flask import request

class Events(Resource):
    def post(self):
        data = request.get_json()
        events_service = EventsServices()
        new_event = events_service.get_request(data)
        return new_event, 200

    def get(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass
    