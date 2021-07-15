from app.settings.database import db
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Boolean


class PollsVotesModel(db.Model):
    __tablename__ = "polls_votes"

    id = Column(Integer, primary_key=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    polls_id = Column(Integer, ForeignKey("polls.id"))

    is_yes = Column(Boolean, nullable=False)
