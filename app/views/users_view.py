from http import HTTPStatus
from flask import Blueprint, Response, jsonify, request

from app.models.users_model import UsersModel
from app.settings.database import db
from app.services.users_service import UsersServices
from flask_restful import Resource

class Users(Resource):
    def post(self):
        data = request.get_json()

        new_user = UsersServices.hashing(data)

        db.session.add(new_user)
        db.session.commit()

        return {"name": new_user.name}, HTTPStatus.CREATED



