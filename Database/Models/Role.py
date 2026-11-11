from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.DB_connection import Base

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")