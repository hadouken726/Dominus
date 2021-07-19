from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import DateTime, Integer, String, Text
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from datetime import datetime, timedelta

from marshmallow_sqlalchemy.schema import auto_field


class PollsModel(db.Model):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True)

    start_at = Column(DateTime, default=datetime.utcnow())
    end_at = Column(DateTime, default=(datetime.utcnow() + timedelta(days=2)))
    desc = Column(String(1000), nullable=False)
    title = Column(String(50), nullable=False)

    votes = relationship(
        "PollsVotesModel", secondary="poll_options", backref=backref("poll")
    )


class PollsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PollsModel
        load_instance = True
        ordered = True

    # id = auto_field()
    # started_at = auto_field()
    # end_at = auto_field()
    # desc = auto_field()
    # title = auto_field()
    # votes = auto_field()
