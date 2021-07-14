from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import request

from app.models.notices_model import NoticesModel
from http import HTTPStatus
from flask_restful import Resource, reqparse
import sqlalchemy.exc as e

from app.settings.database import db


class Notices(Resource):
    def get(self, notice_id=None):
        if notice_id is None:
            notices = NoticesModel()
            query = notices.query.all()
            print(query)
            return {"Notices": [
                {"Title": notices.title, "Description": notices.desc,
                 "Updated_at": notices.updated_at.strftime("%d/%m/%Y")}
                for notices in query]}, HTTPStatus.OK
        else:
            try:
                notice = NoticesModel().query.get(notice_id)
                return {"Notice":
                            {"Title": notice.title, "Description": notice.desc,
                             "Updated_at": notice.updated_at.strftime("%d/%m/%Y")}
                        }, HTTPStatus.OK
            except e.DataError:

                return {"Message": "Invalid number, just accept int with register ids",
                        "Error": "DataError"}, HTTPStatus.BAD_REQUEST

            except AttributeError:
                return {"Message": "Invalid number, just accept int with register ids",
                        "Error": "Attribute Error"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if "teste" == "teste":
            try:
                data = request.get_json(force=True)
                parser = reqparse.RequestParser()
                parser.add_argument("title", type=str, required=True)
                parser.add_argument("desc", type=str, required=True)
                args = parser.parse_args()
                db.session.add(NoticesModel(**args))
                db.session.commit()

                return args

            except:
                return {"Error": " Devs is coding..."}
