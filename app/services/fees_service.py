from functools import partial
from app.models.fees_model import FeeSchema, FeesModel
from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import current_user
from app.models.events_invitations_model import EventInvitationSchema, EventsInvitationsModel
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity
from flask import current_app, request
from flask_restful import abort
from app.models.users_model import UsersModel
from app.models.events_model import EventsModel, EventSchema
from marshmallow import ValidationError, error_store
from typing import List
from marshmallow import Schema, fields
import sqlalchemy.exc as e
from app.services.base_service import BaseService

class FeesService(BaseService):

    def __init__(self, current_user_id, current_app) -> None:
        super().__init__(current_user_id, current_app)

    def post(self, request_data):
        if self.current_user.is_admin:
            try:
                fee_to_post = FeeSchema().load(request_data, session=self.session)
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
            self.add_to_database(fee_to_post)
            return FeeSchema().dump(fee_to_post), HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message='Access allowed only for admins!')
    

    def patch(self, fee_id):
        request_data = request.get_json()
        fetched_fee = FeesModel.query.get_or_404(fee_id)
        if self.current_user.is_admin:
            try:
                fee_to_patch = FeeSchema(exclude=['home_id']).load(request_data, session=self.session, instance=fetched_fee, partial=True)
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
            self.add_to_database(fee_to_patch)
            return FeeSchema().dump(fee_to_patch), HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin can patch a fee!')

    def delete(self, fee_id):
        fee_to_delete = FeesModel.query.get_or_404(fee_id)
        if self.current_user.is_admin:
            self.delete_from_database(fee_to_delete)
            return '', HTTPStatus.NO_CONTENT
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin can delete a fee!')

    def get_all(self):
        all_fees = FeesModel.query.all()
        current_user_fees = FeesModel.query.filter_by(home_id=self.current_user.home_id)
        if self.current_user.is_admin:
            return FeeSchema().dump(all_fees, many=True), HTTPStatus.OK
        return FeeSchema().dump(current_user_fees, many=True), HTTPStatus.OK

    def get_one(self, fee_id):
        fee = FeesModel.query.get_or_404(fee_id)
        if self.current_user.is_admin or fee.home_id == self.current_user.id:
            return FeeSchema().dump(fee), HTTPStatus.OK
        abort(HTTPStatus.UNAUTHORIZED, message='Fee does not belong to the user')
        



        
        
