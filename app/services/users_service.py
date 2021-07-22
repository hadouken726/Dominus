from app.models.homes_model import HomesModel
from app.models.events_model import EventsModel
from functools import partial
from http import HTTPStatus
from flask import request, current_app
from flask_restful import abort
from marshmallow.utils import pprint
from sqlalchemy.util.langhelpers import only_once
from app.models.users_model import UserSchema, UsersModel
from app.models.events_invitations_model import EventsInvitationsModel, EventInvitationSchema 
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash


class UsersService:

    
    def __init__(self, current_user_id) -> None:
        fetched_user = UsersModel.query.get(current_user_id)
        if fetched_user:
            if fetched_user.is_admin:
                self.current_user = fetched_user
                self.session = current_app.db.session
            else:
                abort(HTTPStatus.UNAUTHORIZED, 'Only admin users can register new users!')
        else:
            abort(HTTPStatus.BAD_REQUEST, message='Invalid user!')
    

    def post(self, request_data):
        try:
            new_user = UserSchema().load(request_data, session=self.session)
        except ValidationError as VE:
            abort(HTTPStatus.BAD_REQUEST, message=VE.messages)
        if not HomesModel.query.filter_by(id=new_user.home_id).first():
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='Home does not exists!')
        if UsersModel.query.filter(UsersModel.is_home_in_possession, UsersModel.home_id == new_user.home_id).first():
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, message='Home already has a representative!')
        pass_entry = new_user.password
        new_user.password = generate_password_hash(pass_entry)
        self.session.add(new_user)
        self.session.commit()
        return UserSchema().dump(new_user), HTTPStatus.CREATED

    def get_all(self):
        fetched_users = UsersModel.query.all()
        if self.current_user.is_admin:
            users = UserSchema().dump(fetched_users, many=True)
            return users, HTTPStatus.OK
        users = UserSchema(only=['phone', 'name', 'is_admin']).dump(fetched_users, many=True)
        return users, HTTPStatus.OK
    
    def get_one(self, user_id: int):
        fetched_user = UsersModel.query.get_or_404(user_id)
        if fetched_user.is_admin:
            user = UserSchema().dump(fetched_user)
            return user
        user = UserSchema(only=['phone', 'name', 'is_admin']).dump(fetched_user)
        return user, HTTPStatus.OK

    def delete(self, user_id):
        user_to_delete = UsersModel.query.get_or_404(user_id)
        if self.current_user.is_admin:
            self.session.delete(user_to_delete)
            self.commit()
            return '', HTTPStatus.NO_CONTENT
        abort(HTTPStatus.UNAUTHORIZED, message='Only admin users can delete an user!')

    def patch(self, user_id):
        user_to_patch = UsersModel.query.get_or_404(user_id)
        data_entry = request.get_json()
        if self.current_user.id == user_to_patch.id:
            try:
                updated_user = UserSchema(only=['password']).load(data_entry, instance=user_to_patch, session=self.session, partial=True)
                updated_user.password = generate_password_hash(data_entry['password'])
                self.session.add(updated_user)
                self.session.commit()
                return UserSchema().dump(updated_user), HTTPStatus.OK
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)    
        if self.current_user.is_admin:
            try:
                updated_user = UserSchema(exclude=['password']).load(data_entry, instance=user_to_patch, session=self.session, partial=True)
                self.session.add(updated_user)
                self.session.commit()
                return UserSchema().dump(updated_user), HTTPStatus.OK
            except ValidationError as VE:
                abort(HTTPStatus.BAD_REQUEST, message=VE.messages)   
        abort(HTTPStatus.UNAUTHORIZED, message='Edit allowed only for admin or own user!')
        
        

    

