from flask import Flask
from datetime import timedelta

def init_app(app: Flask):
    from environs import Env

    env = Env()
    env.read_env()
    app.config["JSON_SORT_KEYS"] = False
    app.config['JWT_SECRET_KEY'] = env('JWT_SECRET_KEY')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
