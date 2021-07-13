from http import HTTPStatus
from flask import Blueprint, Response, jsonify, request

from app.models.users_model import UsersModel
from app.settings.database import db
from app.services.users_service import UsersServices
bp = Blueprint('bp_users_route', __name__)


@bp.post('/users')
def create_user():
    data = request.get_json()

    new_user = UsersServices.hashing(data)

    db.session.add(new_user)
    db.session.commit()

    return {"name": new_user.name}, HTTPStatus.CREATED



