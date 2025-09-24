from sqlalchemy import Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)   # PK de la tabla
    user_name = Column(String, nullable=False)
    user_email = Column(String, unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=True)
    recommendations = Column(String, nullable=True)
    ZIP = Column(String, nullable=True)




