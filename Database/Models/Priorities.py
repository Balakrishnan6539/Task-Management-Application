from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Database.DB_connection import Base

class Priorities(Base):
    __tablename__ = "priorities"

    priority_id = Column(Integer, primary_key=True, index=True)
    priority_name = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="priority_rel")
    