from datetime import datetime, timedelta
from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class EventsModel(db.Model):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(50), nullable=False)
    desc = Column(String(5000), nullable=False)
    start_at = Column(DateTime, default=datetime.utcnow())
    end_at = Column(DateTime, default=datetime.utcnow() + timedelta(hours=1))
    is_important = Column(Boolean, default=False)


class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventsModel
        load_instance = True
        include_fk = True
        update_fields = ('title', 'desc', 'start_at', 'end_at',)
    id = auto_field('id', dump_only=True)
    host_id = auto_field('host_id', dump_only=True)
