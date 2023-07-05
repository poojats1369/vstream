from api.db import *
from utils import *
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

class Otp(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    phone_no = Column(String,unique = True,index=True)
    phone_code = Column(String)
    email = Column(String,unique = True,index=True)
    otp_code = Column(Integer,nullable=False)
    expiry_datetime = Column(DateTime)
    no_of_attempts = Column(Integer,nullable=False)
    is_expired = Column(Boolean,nullable=False, default = False) 