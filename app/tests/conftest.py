import pytest
from app import create_app
from app.models.users_model import UsersModel


@pytest.fixture(scope='module')
def app():
    """
    Instância do app
    """
    return create_app()