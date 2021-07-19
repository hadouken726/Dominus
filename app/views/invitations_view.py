from flask_restful import Resource
from app.services.invitations_service import InvitationsService

class Invitations(Resource):
    def get(self):
        pass

    def patch(self, invitation_id):
        invitations_service = InvitationsService(3)
        response = invitations_service.patch(invitation_id)
        return response
    def delete(self, invitation_id):
        return InvitationsService(1).delete(invitation_id)
    