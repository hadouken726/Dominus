from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text
from app.settings.database import db
from sqlalchemy.schema import Column
from datetime import datetime, timedelta


class PollOptionsModel(db.Model):
    __tablename__ = "poll_options"

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('polls.id'))
    name = Column(String, nullable=False)