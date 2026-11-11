from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Database.DB_connection import Base
from datetime import datetime, timezone


class Activity_log(Base):
    __tablename__ = "activity_log"

    log_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    action = Column(String)
    field_name = Column(String)
    old_value = Column(String)
    new_value = Column(String)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="activity_logs")