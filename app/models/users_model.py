from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import CHAR, Integer, String, Boolean
from sqlalchemy.schema import Column
from werkzeug.security import generate_password_hash, check_password_hash

from app.settings.database import db


class UsersModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    home_id = Column(Integer, ForeignKey('homes.id'))
    cpf = Column(CHAR(11), nullable=False, unique=True)
    phone = Column(String(11), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    password = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)

    @property
    def password_hash(self):
        raise AttributeError("Password cannot be accessed!")

    @password_hash.setter
    def password_hash(self, password_to_hash):
        self.password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare) -> Boolean:
        return check_password_hash(self.password_hash, password_to_compare)
