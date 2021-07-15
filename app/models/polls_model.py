from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text
from app.settings.database import db
from sqlalchemy.schema import Column
from datetime import datetime, timedelta


class PollsModel(db.Model):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)

    start_at = Column(DateTime, default=datetime.utcnow())
    end_at = Column(DateTime, default=(datetime.utcnow() + timedelta(days=2)))
    desc = Column(String, nullable=False)
    title = Column(String, nullable=False)

    votes = relationship('PollsVotesModel', secondary='poll_options', backref=backref('poll'))
    options = relationship('PollOptionsModel', backref=backref('poll'))