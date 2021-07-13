from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from app.settings.database import db
from sqlalchemy.schema import Column


class UsersModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    cpf = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    # TODO Create new Column = Bloco da residencia
    home_number = Column(Integer, nullable=False)
