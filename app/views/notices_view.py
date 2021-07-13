from flask import Blueprint



bp = Blueprint('bp_notices_route', __name__)


@bp.get('/notices')
def all_notices():
    return 'Running', 200