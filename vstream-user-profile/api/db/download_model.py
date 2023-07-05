from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from utils import Base

class DownloadList(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    download_id = Column(String, index=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    profile_id = Column(String, ForeignKey("user_profiles.profile_id"))
    content_id = Column(String, ForeignKey("content.content_id"))
    device_id = Column(String, ForeignKey("devices.device_id"))
    location = Column(String)
    created_at = Column(DateTime, default=func.now())
    expiry_datetime = Column(DateTime)
    is_expired = Column(Boolean, nullable=False, default=False)
    download_url = Column(String)
    download_size = Column(String)
    download_quality = Column(String)
    download_format = Column(String)
    subtitle_language = Column(String)
    audio_language = Column(String)
    download_duration = Column(String)

    user = relationship("User", back_populates="downloads")
    content = relationship("Content", back_populates="downloads")
    device = relationship("Device", back_populates="downloads")
    profile = relationship("UserProfile", back_populates="downloads")
