from http import HTTPStatus
from typing import Tuple

from flask import Blueprint, Response, jsonify

from app.models.notices_model import NoticesModel

bp = Blueprint('bp_notices_route', __name__)


@bp.get('/notices')
def get_notices() -> Tuple[Response, int]:
    notices = NoticesModel()
    query = notices.query.all()
    return jsonify({"Notices": [
        {"Title": notices.title, "Description": notices.desc, "Updated_at": notices.updated_at.strftime("%d/%m/%Y")}
        for notices in query]}), HTTPStatus.OK


@bp.get('/notices/<int:notice_id>')
def get_notice_by_id(notice_id) -> Tuple[Response, int]:
    notice = NoticesModel().query.get(notice_id)
    return jsonify({"Notice":
                        {"Title": notice.title, "Description": notice.desc,
                         "Updated_at": notice.updated_at.strftime("%d/%m/%Y")}}
                   ), HTTPStatus.OK
