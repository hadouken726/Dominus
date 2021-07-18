from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Enum, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class EventsInvitationsModel(db.Model):
    __tablename__ = 'events_invitations'
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    guest_id = Column(Integer, ForeignKey('users.id'))
    status = Column(Enum('invited', 'accepted', 'rejected', name='status'), default='invited')
    guest = relationship('UsersModel', backref=backref('received_invitations'))
    event = relationship('EventsModel', backref=backref('sended_invitations'))

class EventInvitationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventsInvitationsModel
        load_instance = True
        include_fk = True
    id = auto_field('id', dump_only=True)