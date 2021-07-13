from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from app.settings.database import db
from sqlalchemy.schema import Column
from datetime import datetime


class NoticesModel(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
