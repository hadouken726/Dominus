from http import HTTPStatus
from flask import Blueprint, Response, jsonify, request
from flask_restful import Resource

from app.models.users_model import UsersModel
from app.settings.database import db
from app.services.users_service import UsersServices



class Users(Resource):
    def post(self):
        data = request.get_json()

        new_user = UsersServices.hashing(data)

        db.session.add(new_user)
        db.session.commit()

        return {"name": new_user.name}, HTTPStatus.CREATED

    def get(self):
        users = UsersModel()
        query = users.query.all()

        return {
                "users": [
                       {"id": user.id, "name": user.name, "phone": user.phone, "home_number": user.home_number}
                       for user in query
                   ]
               }, HTTPStatus.ACCEPTED

    def get(self, user_id: int):
        user = UsersModel()
        user = user.query.get(user_id)

        return {
            "id": user.id, "name": user.name, "phone": user.phone, "home_number": user.home_number
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

        return {"id": query.id, "name": query.name, "phone": user.phone, "home_number": user.home_number}





