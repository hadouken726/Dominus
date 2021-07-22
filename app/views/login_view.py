from flask import jsonify, request
from http import HTTPStatus
from sqlalchemy.orm import query
from app.models.users_model import UserSchema, UsersModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from app.services.login_service import LoginService


class Login(Resource):
    def post(self):
        request_data = request.get_json()
        login_service = LoginService()
        login_data = login_service.get_data(request_data)
        logged_user = login_service.get_user_from(login_data.cpf, login_data.password)
        access_token = login_service.generate_token(logged_user.id)
        return jsonify(access_token=access_token)
