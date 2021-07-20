from flask_restful import Resource
from app.services.invitations_service import InvitationsService
from flask_jwt_extended import jwt_required, get_jwt_identity

class Invitations(Resource):
    @jwt_required()
    def get(self, invitation_id=None):
        current_user_id = get_jwt_identity()
        invitation_service = InvitationsService(current_user_id)
        if not invitation_id:
            return invitation_service.get_all()
        return invitation_service.get_one(invitation_id)

    @jwt_required()
    def patch(self, invitation_id):
        invitations_service = InvitationsService(3)
        return invitations_service.patch(invitation_id)
    

    @jwt_required()    
    def delete(self, invitation_id):
        return InvitationsService(1).delete(invitation_id)
    