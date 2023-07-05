from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from utils import Base

class CmsUsers(Base):
    __tablename__ = "Cms_Users"

    id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    emp_id = Column(String)
    password = Column(String, nullable=False)
    role = Column(String, default="Subscriber")
    phone = Column(String, nullable=False, unique=True)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=func.now())
    is_active = Column(Boolean, default=False)
    otp_table = relationship("OtpTable", back_populates="user")


class Token(Base):
    __tablename__ = "Tokens"

    id = Column(String, primary_key=True)
    device_id = Column(String, unique=True)
    access_token = Column(String)
    user_id = Column(String, ForeignKey('Cms_Users.id'), nullable=False)
    cms_user = relationship(CmsUsers)

class OtpTable(Base):
    __tablename__ = "Otp_Table"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('Cms_Users.id'), nullable=False)
    phone_code = Column(String)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    otp_code = Column(String, nullable=False)
    expiry_date = Column(DateTime)
    no_of_attempts = Column(Integer, nullable=False)
    is_expired = Column(Boolean, nullable=False, default=False)
    user = relationship("CmsUsers", back_populates="otp_table")

class UserRoles(Base):
    __tablename__ = "User_Roles"
    
    id = Column(String, primary_key=True)
    role_name = Column(String, nullable=False)
    permissions = Column(postgresql.ARRAY(String), nullable=True)
    status = Column(Boolean, default=True)

class UserPermissions(Base):
    __tablename__ = "User_Permissions"

    id = Column(String, primary_key=True)
    permission_name = Column(String, nullable=False)
    permission_type = Column(String, nullable=False)
    collection = Column(postgresql.ARRAY(String), nullable=False)
    status = Column(Boolean, default=False)
