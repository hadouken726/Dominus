from flask import Blueprint



bp = Blueprint('bp_test', __name__)


@bp.get('/test')
def test():
    return 'Hello world!', 200