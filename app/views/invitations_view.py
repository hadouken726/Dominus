from flask_restful import Resource
from app.services.invitations_service import InvitationsService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask import current_app


class Invitations(Resource):
    @jwt_required()
    def get(self, invitation_id=None):
        current_user_id = get_jwt_identity()
        invitation_service = InvitationsService(current_user_id, current_app)
        if not invitation_id:
            return invitation_service.get_all()
        return invitation_service.get_one(invitation_id)

    @jwt_required()
    def patch(self, invitation_id):
        current_user_id = get_jwt_identity()
        invitations_service = InvitationsService(current_user_id, current_app)
        return invitations_service.patch(invitation_id)
    

    @jwt_required()    
    def delete(self, invitation_id):
        current_user_id = get_jwt_identity()
        return InvitationsService(current_user_id, current_app).delete(invitation_id)

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        new_invitation = request.get_json()
        return InvitationsService(current_user_id, current_app).post(new_invitation)
    
    