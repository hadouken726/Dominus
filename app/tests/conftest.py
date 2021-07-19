import pytest
from app import create_app
from app.models.users_model import UsersModel


@pytest.fixture(scope='module')
def app():
    """
    Instância do app
    """
    return create_app()

# @pytest.fixture(scope='module')
# def new_user():
#     user = UsersModel(cpf='00011122212', phone='11992999999', password='123')
#     return user