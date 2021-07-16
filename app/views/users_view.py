from http import HTTPStatus
from flask import Blueprint, Response, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.users_model import UsersModel
from app.settings.database import db
from app.services.users_service import UsersServices



class Users(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        is_admin = UsersModel.query.get(user_id).is_admin
        if is_admin:
            data = request.get_json()

            new_user = UsersServices.hashing(data)

            db.session.add(new_user)
            db.session.commit()

            return {"name": new_user.name}, HTTPStatus.CREATED
        return {'msg': 'permission denied!'}


    def get(self, user_id=None):
        
        if user_id is None:
            users = UsersModel().query.all()

            return {
                    "users": [
                        {"id": user.id, "name": user.name, "phone": user.phone}
                        for user in users
                    ]
                }, HTTPStatus.ACCEPTED
        else:
            user = UsersModel().query.get(user_id)

            return {
                "id": user.id, "name": user.name, "phone": user.phone, "home_number": user.home.number
            }

    def delete(self, user_id: int):
        user = UsersModel()
        query = user.query.get(user_id)

        db.session.delete(query)
        db.session.commit()

    def patch(self, user_id: int):
        data = request.get_json()

        user = UsersModel()

        query = user.query.get(user_id)

        for key, value in data.items():
            setattr(query, key, value)

        db.session.add(query)
        db.session.commit()

        return {"id": query.id, "name": query.name, "phone": query.phone, "home_number": query.home.number}





