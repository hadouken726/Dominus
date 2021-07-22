from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime, Enum, Float, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class FeesModel(db.Model):
    __tablename__ = 'fees'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(50), default='Taxa de condomínio')
    home_id = Column(Integer, ForeignKey('homes.id'))
    due_date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    payment_date = Column(Date, default=None)
    home = relationship('HomesModel', backref=backref('fees'))
    

class FeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FeesModel
        load_instance = True
        include_fk = True
    id = auto_field('id', dump_only=True)