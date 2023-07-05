import enum
from api.db import *
from utils import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, TIMESTAMP, Enum as EnumSQL

class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(String,index=True,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    email = Column(String,unique = True,index=True)
    phone_no = Column(String,unique = True,index=True)
    phone_code = Column(String)
    email_verified = Column(Boolean, default = False)
    phone_verified = Column(Boolean, default = False)
    social_id = Column(String)
    social_type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    app_language = Column(String, default = "English")
    # gender = Column(EnumSQL(GenderEnum), nullable = True)
    gender = Column(String)
    profile_image = Column(Text)
    bio = Column(Text)
    longitude = Column(String)
    latitude = Column(String)
    last_login_datetime = Column(DateTime)
    status = Column(Boolean)

    profiles = relationship("UserProfile", back_populates="user", cascade="all, delete, delete-orphan")
    watchlist_items = relationship("WatchlistItem", back_populates="user")

