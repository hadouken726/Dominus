from http import HTTPStatus
import sqlalchemy.exc as e
from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.orm import session

from app.models.homes_model import HomesModel, HomeSchema
from app.settings.database import db


class Homes(Resource):
    def get(self, home_id=None):
        if home_id is None:
            homes = HomesModel().query.all()
            return {"Homes": HomeSchema(many=True).dump(homes)}, HTTPStatus.OK
        else:
            try:
                homes = HomesModel().query.get_or_404(home_id)
                homes_schema = HomeSchema()
                return homes_schema.dump(homes), HTTPStatus.OK

            except e.DataError:

                return {"message": "invalid number, just accept int with register ids",
                        "error": "dataError"}, HTTPStatus.BAD_REQUEST


    @jwt_required()
    def delete(self, home_id=None):
        is_admin = get_jwt_identity()
        if is_admin:
            home = HomesModel().query.get_or_404(home_id)
            db.session.delete(home)
            db.session.commit()
            return {"message": f"home {home.id} has been deleted"}

        if not is_admin:
            return {"message": "user dont have admin permission to create a new home"}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def patch(self, home_id=None):

        is_admin = get_jwt_identity()
        if is_admin:
            try:
                data = request.get_json()
                home = HomesModel().query.get_or_404(home_id)
                updated_home = HomeSchema().load(data, instance=home, partial=True, session=session)
                db.session.add(updated_home)
                db.session.commit()
                return HomeSchema().dump(updated_home), HTTPStatus.OK

            except ValidationError as VE:
                return VE.messages

        if not is_admin:
            return {"message": "user dont have admin permission to create a new home"}, HTTPStatus.UNAUTHORIZED


    @jwt_required()
    def post(self):
        is_admin = get_jwt_identity()
        if is_admin:
            try:
                session = current_app.db.session
                data = request.get_json()
                home_schema = HomeSchema()
                new_home = home_schema.load(data, session=session)
                session.add(new_home)
                session.commit()
                return home_schema.dump(new_home)

            except ValidationError as VE:
                return VE.messages

            except e.IntegrityError as error:

                return str(error.__dict__["orig"]), HTTPStatus.BAD_REQUEST

        if not is_admin:
            return {"message": "user dont have admin permission to create a new home"}, HTTPStatus.UNAUTHORIZED

