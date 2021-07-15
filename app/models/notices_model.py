from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from app.settings.database import db, ma
from sqlalchemy.schema import Column
from datetime import datetime


class NoticesModel(db.Model):
    __tablename__ = "notices"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

class NoticeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoticesModel
        load_instance = True
        ordered = True
    id = auto_field('id', dump_only=True)
    updated_at = auto_field('updated_at', dump_only=True)
