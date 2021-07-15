from flask.json import jsonify, load
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, current_app
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm import session
from app.models.notices_model import NoticesModel, NoticeSchema
from marshmallow import pre_load
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e
import json

from app.settings.database import db


class Notices(Resource):
    def get(self, notice_id=None):
        if notice_id is None:
            notices = NoticesModel().query.all()
            notices_schema = NoticeSchema(many=True)
            return notices_schema.dump(notices), HTTPStatus.OK
        else:
            try:
                notice = NoticesModel().query.get(notice_id)
                notice_schema = NoticeSchema()
                return notice_schema.dump(notice), HTTPStatus.OK
            except e.DataError:

                return {"Message": "Invalid number, just accept int with register ids",
                        "Error": "DataError"}, HTTPStatus.BAD_REQUEST

            except AttributeError:
                return {"Message": "Invalid number, just accept int with register ids",
                        "Error": "Attribute Error"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        try:
            session = current_app.db.session
            data = request.get_json()
            notice_schema = NoticeSchema()
            new_notice = notice_schema.load(data, session=session)
            session.add(new_notice)
            session.commit()
            return notice_schema.dump(new_notice)

        except ValidationError as VE:
            return VE.messages
