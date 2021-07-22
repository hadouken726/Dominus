from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime, Enum, Float, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class SpendingsModel(db.Model):
    __tablename__ = 'spendings'
    
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('spendings_categories.id'))
    value = Column(Float, nullable=False)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    category = relationship('SpendingsCategoriesModel', backref=backref('spendings'))
    

class SpendingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpendingsModel
        load_instance = True
        include_fk = True
    id = auto_field('id', dump_only=True)