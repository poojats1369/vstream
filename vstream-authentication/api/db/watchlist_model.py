from utils import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float,String

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    watchlist_id = Column(String,index=True,unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    user_profile_id = Column(String, ForeignKey("user_profiles.profile_id"))
    # content_id = Column(String, ForeignKey("content.content_id"))
    content_id = Column(String)
    watch_progress=  Column(String)
    # watch_progress = Column(Float(asdecimal=True))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_profile = relationship("UserProfile", back_populates="watchlist_items")
    user = relationship("User", back_populates="watchlist_items")
    # content = relationship("Content", back_populates="watchlist_items")

    def __repr__(self):
        return f"<WatchlistItem(id={self.id}, user_id={self.user_id}, content_id={self.content_id})>"