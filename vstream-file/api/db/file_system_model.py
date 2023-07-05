
from utils import *
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Text, Float, Enum 

class FileSystem(Base):
    __tablename__ = "FileSystem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String(80), index=True, unique=True, nullable=False)
    object_id = Column(String(80), nullable=False)
    object_type = Column(String(80), nullable=False)
    file_name = Column(String(80), nullable=False)
    path = Column(String(200), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    status = Column(Integer, default=1)
    file_size = Column(BigInteger, nullable=False)  # File size in bytes
    mime_type = Column(String(100), nullable=True)  # Mime type of the file
    duration = Column(Float, nullable=True)  # Duration of the file in seconds
    thumbnail_path = Column(String(200), nullable=True)  # Path to the thumbnail image
    description = Column(Text, nullable=True)  # Description or additional information about the file
    is_public = Column(Boolean, default=False)

    def __repr__(self):
        return f"<FileSystem(id={self.id}, file_name='{self.file_name}', file_id={self.file_id})>"
