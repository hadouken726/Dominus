from flask import jsonify, request
from http import HTTPStatus
from sqlalchemy.orm import query
from app.models.users_model import UsersModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token

class Login(Resource):

    """
        [X] Rota POST de autenticação
        [ ] Rota POST protegida
    """

    def post(self):
        user : UsersModel = UsersModel()
        found_user : UsersModel = user.query.filter_by(cpf=user.cpf).first_or_404()

        if not found_user:
            return {"message": "user not found"}, HTTPStatus.NOT_FOUND
        
        if not found_user.check_password(user.password):
            return jsonify({"error": "wrong credentials"}), HTTPStatus.FORBIDDEN

        payload = {
            "id": user.id,
            "name": user.name
        }

        access_token = create_access_token(identity=payload)

        return jsonify(access_token=access_token)

