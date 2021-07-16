from flask import Flask


def init_app(app: Flask):
    from environs import Env

    env = Env()
    env.read_env()
    app.config["JSON_SORT_KEYS"] = False
    app.config['JWT_SECRET_KEY'] = env('JWT_SECRET_KEY')
