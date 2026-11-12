from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from Database.DB_connection import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    mobile_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.role_id",ondelete="SET NULL"), default=3)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    updated_by = Column(Integer, ForeignKey("users.user_id",ondelete="SET NULL"), nullable=True)


    role = relationship("Role", back_populates="users")
    projects = relationship("Project_Member", back_populates="user")
    tasks = relationship("Task", back_populates="assigned_user")
    created_tasks = relationship("Task", back_populates="creator")
    comments = relationship("Task_Comments", back_populates="user")
    activity_logs = relationship("Activity_log", back_populates="user")