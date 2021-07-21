from functools import partial
from app.models.spendings_model import SpendingsModel, SpendingSchema
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



class SpendingsService:

    
    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get_or_404(current_user_id)
        self.current_user = fetched_user
        self.session = current_app.db.session


    def post(self, request_data):
        if self.current_user.is_admin:
            try:
                spending_to_post = SpendingSchema().load(request_data, session=self.session)
                self.session.add(spending_to_post)
                self.session.commit()
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
            return SpendingSchema().dump(spending_to_post), HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message='Only admins can post a spending!')
    

    def patch(self, spending_id):
        request_data = request.get_json()
        fetched_spending = SpendingsModel.query.get_or_404(spending_id)
        if self.current_user.is_admin:
            try:
                spending_to_patch = SpendingSchema().load(request_data, session=self.session, instance=fetched_spending, partial=True)
                self.session.add(spending_to_patch)
                self.session.commit()
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
            return SpendingSchema().dump(spending_to_patch), HTTPStatus.CREATED
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin can patch a spending!')

    def delete(self, spending_id):
        spending_to_delete = SpendingsModel.query.get_or_404(spending_id)
        if self.current_user.is_admin:
            self.session.delete(spending_to_delete)
            self.session.commit()
            return '', HTTPStatus.NO_CONTENT
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin can delete a spending!')

    def get_all(self):
        all_spendings = SpendingsModel.query.all()
        return SpendingSchema().dump(all_spendings, many=True), HTTPStatus.OK
        

    def get_one(self, fee_id):
        return SpendingsModel.query.get_or_404(fee_id)



        
        
