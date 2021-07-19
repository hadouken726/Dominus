
import tempfile
import os
import pytest

from app import create_app
from app.settings.database import init_app

def test_login(client):
    
    rv = client.get('/notices')
    assert b'{"notices": []}\n' == rv.data
