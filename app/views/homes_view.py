from http import HTTPStatus
import sqlalchemy as e
from flask_restful import Resource
from app.models.homes_model import HomesModel, HomeSchema

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