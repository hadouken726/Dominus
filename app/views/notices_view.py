from http import HTTPStatus

from flask import Blueprint

from app.models.notices_model import NoticesModel

bp = Blueprint('bp_notices_route', __name__)


@bp.get('/notices')
def get_notices():
    notices = NoticesModel()
    query = notices.query.all()
    return {"Notices": [
        {"Title": notices.title, "Description": notices.desc, "Updated_at": notices.updated_at.strftime("%d/%m/%Y")}
        for notices in query]}, HTTPStatus.OK
