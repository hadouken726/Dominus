from app.models.users_model import UsersModel
from sqlalchemy.orm import backref, relationship
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Boolean
from marshmallow_sqlalchemy.schema import auto_field
from marshmallow_sqlalchemy import fields


class PollsVotesModel(db.Model):
    __tablename__ = "polls_votes"

    id = Column(Integer, primary_key=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    option_id = Column(Integer, ForeignKey("poll_options.id"))
    owner = relationship("UsersModel", backref=backref("votes"))
    option = relationship("PollOptionsModel", backref=backref("votes"))


class PollVoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PollsVotesModel
        load_instance = True
        ordered = True

    id = auto_field("id", dump_only=True)
