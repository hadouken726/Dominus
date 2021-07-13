from app.models.notices_model import NoticesModel
from http import HTTPStatus
from flask_restful import Resource
import sqlalchemy.exc as e

class Notices(Resource):
    def get(self, notice_id=None):
        if notice_id is None:
            notices = NoticesModel()
            query = notices.query.all()
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
            