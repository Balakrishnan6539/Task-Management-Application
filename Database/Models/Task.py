from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime,timezone
from Database.DB_connection import Base

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    assigned_to = Column(Integer, ForeignKey("users.user_id",ondelete="SET NULL"),nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    title = Column(String)
    description = Column(String)
    priority = Column(String,ForeignKey("priorities.priority_name", ondelete="SET NULL"))
    status = Column(String,ForeignKey("status.status_name", ondelete="SET NULL"))
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    project = relationship("Project", back_populates="tasks")
    assigned_user = relationship("User", foreign_keys=[assigned_to], back_populates="tasks")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_tasks")
    priority_rel = relationship("Priorities", back_populates="tasks")
    status_rel = relationship("Task_Status", back_populates="tasks")
    comments = relationship("Task_Comments", back_populates="task")