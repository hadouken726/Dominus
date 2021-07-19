from flask import jsonify, request
from http import HTTPStatus
from sqlalchemy.orm import query
from app.models.users_model import UsersModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token
# from ipdb import set_trace

# from ipdb import set_trace


class Login(Resource):

    """
    [X] Rota POST de autenticação
    [ ] Rota POST protegida
    """

    def post(self):
        user_data = request.get_json()
        user = UsersModel()
        found_user = user.query.filter_by(cpf=user_data["cpf"]).first_or_404()

        payload_id = {"id": found_user.id}

        access_token = create_access_token(identity=payload_id)

        return jsonify(access_token=access_token)
