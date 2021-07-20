from sqlalchemy.sql.expression import update
from sqlalchemy.sql.functions import current_user
from app.models.events_invitations_model import EventInvitationSchema, EventsInvitationsModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from flask import current_app, request
from flask_restful import abort
from app.models.users_model import UserSchema, UsersModel
from app.models.events_model import EventsModel, EventSchema
from marshmallow import ValidationError, error_store
from typing import List
from marshmallow import Schema, fields
from  werkzeug.security import check_password_hash






class LoginService:
        
    def get_data(self, request_data):
        try:
            login_data = UserSchema(only=['cpf', 'password']).load(request_data)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
        return login_data
    

    def _get_user_from_cpf(self, cpf_entry):
        fetched_user = UsersModel.query.filter_by(cpf=cpf_entry).first()
        if not fetched_user:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid CPF!')
        return fetched_user


    def get_user_from(self, cpf: str, pass_entry: str):
        fetched_user = self._get_user_from_cpf(cpf)
        is_pass_ok = check_password_hash(fetched_user.password, pass_entry)
        if not is_pass_ok:
            abort(HTTPStatus.UNAUTHORIZED, message='Invalid password!')
        return fetched_user
    
    def generate_token(self, jwt_identity: int):
        return create_access_token(identity=jwt_identity)

    

    


        
        
