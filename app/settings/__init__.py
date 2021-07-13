from flask import Flask


def init_app(app: Flask):
    from environs import Env

    env = Env()
    env.read_env()
    app.config["JSON_SORT_KEYS"] = False
