from flask_restful import Resource
from flask import request
from app.services.fees_service import FeesService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app


class Fees(Resource):
    @jwt_required()
    def get(self, fee_id=None):
        current_user_id = get_jwt_identity()
        fees_service = FeesService(current_user_id, current_app)
        if not fee_id:
            return fees_service.get_all()
        return fees_service.get_one(fee_id)

    @jwt_required()
    def patch(self, fee_id):
        current_user_id = get_jwt_identity()
        fees_service = FeesService(current_user_id, current_app)
        return fees_service.patch(fee_id)
    

    @jwt_required()    
    def delete(self, fee_id):
        current_user_id = get_jwt_identity()
        return FeesService(current_user_id, current_app).delete(fee_id)

    @jwt_required()
    def post(self):
        fee_entry = request.get_json()
        current_user_id = get_jwt_identity()
        return FeesService(current_user_id, current_app).post(fee_entry)