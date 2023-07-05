from utils import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, Float

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(String,index=True,unique=True)
    title = Column(String)
    description = Column(Text)
    thumbnail_url = Column(String)
    duration = Column(Float)
    genre = Column(String)
    release_date = Column(String)
    director = Column(String)
    actors = Column(Text)

    watchlist_items = relationship("WatchlistItem", back_populates="content", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}')>"