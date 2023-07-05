from api.db import *
from utils import *
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    device_id = Column(String)
    device_name = Column(String)
    device_type = Column(String)
    os = Column(String)
    os_version = Column(String)
    device_token = Column(Text)
    app_version = Column(String)

    downloads = relationship("DownloadList", back_populates="device", cascade="all, delete, delete-orphan")