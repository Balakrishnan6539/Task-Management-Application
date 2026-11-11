from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from Database.DB_connection import Base

class Status(Base):
    __tablename__ = "status"

    status_id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String, unique=True, index=True)

    projects = relationship("Project", back_populates="status_info")
    tasks = relationship("Task", back_populates="status_rel")