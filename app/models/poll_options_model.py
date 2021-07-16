from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from datetime import datetime, timedelta
from marshmallow_sqlalchemy.schema import auto_field


class PollOptionsModel(db.Model):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('polls.id'))
    name = Column(String(100), nullable=False)

class PollOptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PollOptionsModel
        load_instance = True
        ordered = True
    id = auto_field('id', dump_only=True)