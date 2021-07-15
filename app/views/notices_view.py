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
            return {"notices": notices_schema.dump(notices)}, HTTPStatus.OK
        else:
            try:
                notice = NoticesModel().query.get(notice_id)
                notice_schema = NoticeSchema()
                return notice_schema.dump(notice), HTTPStatus.OK
            except e.DataError:

                return {"message": "invalid number, just accept int with register ids",
                        "error": "dataError"}, HTTPStatus.BAD_REQUEST

            except AttributeError:
                return {"message": "invalid number, just accept int with register ids",
                        "error": "attribute Error"}, HTTPStatus.BAD_REQUEST

    @jwt_required()
    def post(self):
        is_admin = get_jwt_identity()["admin"]
        if is_admin:
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

        if not is_admin:
            return {"message": "user dont have admin permission to create a new notice"}, HTTPStatus.UNAUTHORIZED

    @jwt_required()
    def delete(self, notice_id=None):
        is_admin = get_jwt_identity()["id"]
        if is_admin:
            notice = NoticesModel().query.get(notice_id)
            db.session.delete(notice)
            db.session.commit()
            return {"message": f"notice {notice.id} has been deleted"}

        if not is_admin:
            return {"message": "user dont have admin permission to create a new notice"}, HTTPStatus.UNAUTHORIZED


    @jwt_required()
    def patch(self, notice_id=None):
        try:
            data = request.get_json()
            notice = NoticesModel.query.get_or_404(notice_id)
            for key, value in data.items():
                setattr(notice, key, value)
            notice_schema = NoticeSchema()
            patch_notice = notice_schema.load(data, session=session)
            db.session.add(patch_notice)
            db.session.commit()

            return notice_schema.dump(patch_notice)

        except ValidationError as VE:
            return VE.messages
