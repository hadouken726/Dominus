from flask_marshmallow import fields
from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String

from app.models.users_model import UserSchema
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from datetime import datetime


class HomesModel(db.Model):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False, unique=True)
    area = Column(Float)
    block = Column(String(3))
    residents = relationship('UsersModel', backref=backref('home'))

class HomeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HomesModel
        load_instance = True
        ordered = True

    id = auto_field('id', dump_only=True)
    residents = ma.Nested(UserSchema, many=True, exclude=("id", "cpf", "is_admin", "is_home_in_possession"))
