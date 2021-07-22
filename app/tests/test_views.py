from http.client import BAD_REQUEST, CREATED, INTERNAL_SERVER_ERROR, UNAUTHORIZED
from flask import url_for, Response
from app import create_app
from app.settings.database import init_app


def test_login_invalid_user(client):
    assert client.post(url_for("/login")).status_code == BAD_REQUEST


def test_login_invalid(client):

    headers = {"Authorization": "JWT <token>"}
    res = (
        client.post(
            url_for("/login"), data={"cpf": "111", "password": "123"}
        )
    )

    assert res.status_code == BAD_REQUEST

def test_auth_events(client):
    assert client.get("/events").status_code == INTERNAL_SERVER_ERROR

def test_auth_all_users(client):
    assert client.get("/users").status_code == INTERNAL_SERVER_ERROR
    
def test_notices(client):

    notices = client.get("/notices")
    assert b'{"notices": []}\n' == notices.data
