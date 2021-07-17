from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from app.settings.database import  db, ma
from sqlalchemy.schema import Column



class EventsCategoriesModel(db.Model):
    __tablename__ = 'events_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventsCategoriesModel
        load_instance = True
    id = auto_field('id', dump_only=True)