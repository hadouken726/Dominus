from ipdb.__main__ import set_trace
from marshmallow_sqlalchemy.schema import auto_field
from sqlalchemy.orm import load_only
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import CHAR, Integer, String, Boolean
from sqlalchemy.schema import Column
from werkzeug.security import generate_password_hash, check_password_hash

from app.settings.database import db, ma


class UsersModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey('homes.id'))
    cpf = Column(CHAR(11), nullable=False, unique=True)
    phone = Column(String(11), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    password = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_home_in_possession = Column(Boolean, nullable=False, default=False)

        
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UsersModel
        load_instance = True
        ordered = True
    id = auto_field('id', dump_only=True)
    password = auto_field('password', load_only=True)