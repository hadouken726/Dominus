from os import read
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import false


db = SQLAlchemy()


def init_app(app: Flask):
    from environs import Env
    env = Env()
    env.read_env()
    app.config['SQLALCHEMY_DATABASE_URI'] = env('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.db = db
    from app.models.users_model import UsersModel
    from app.models.notices_model import NoticesModel
    
