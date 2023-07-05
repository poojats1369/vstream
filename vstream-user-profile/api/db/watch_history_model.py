from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float,String
from sqlalchemy.orm import relationship
from utils import Base
from datetime import datetime

class WatchHistoryItem(Base):
    __tablename__ = "watch_history_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    watch_history_id = Column(String,index=True,unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    user_profile_id = Column(String, ForeignKey("user_profiles.profile_id"))
    content_id = Column(String, ForeignKey("content.content_id"))
    watch_duration=  Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_profile = relationship("UserProfile", back_populates="watch_history_items")
    user = relationship("User", back_populates="watch_history_items")
    content = relationship("Content", back_populates="watch_history_items")

    def __repr__(self):
        return f"<WatchHistoryItem(id={self.id}, user_id={self.user_id}, content_id={self.content_id})>"