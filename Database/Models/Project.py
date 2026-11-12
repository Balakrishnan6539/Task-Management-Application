from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Database.DB_connection import Base
from datetime import datetime, timezone

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, unique=True, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(Integer, ForeignKey("status.status_id", ondelete="SET NULL"), default=1)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    tasks = relationship("Task", back_populates="project")
    project_members = relationship("Project_Member", back_populates="project")
    status_info = relationship("Status", back_populates="projects")
    