from sqlalchemy import Column, Integer,ForeignKey, DateTime
from Database.DB_connection import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Project_Member(Base):
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"),primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"),primary_key=True)
    join_date = Column(DateTime, default=datetime.now(timezone.utc))

    project = relationship("Project", back_populates="project_members")
    user= relationship("User", back_populates="projects")