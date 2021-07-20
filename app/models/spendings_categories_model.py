from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime, Enum, Float, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class SpendingsCategoriesModel(db.Model):
    __tablename__ = 'spendings_categories'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    desc = Column(String, nullable=False)
    
    

class SpendingCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpendingsCategoriesModel
        load_instance = True
        include_fk = True
    id = auto_field('id', dump_only=True)