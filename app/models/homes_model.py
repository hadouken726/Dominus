from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Float, Integer, String
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from datetime import datetime


class HomesModel(db.Model):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)
    holder_id = Column(Integer, ForeignKey('users.id'))
    number = Column(Integer, nullable=False, unique=True)
    area = Column(Float)
    block = Column(String(3))
    residents = relationship('UsersModel', backref=backref('home'))