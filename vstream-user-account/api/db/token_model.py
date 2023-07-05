from api.db import *
from utils import *
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text

class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True,autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    login_type = Column(String)
    access_token = Column(Text)
    at_created = Column(DateTime)
    at_updated = Column(DateTime)
    at_expiry = Column(DateTime)
    refresh_token = Column(Text)
    rt_created = Column(DateTime)
    rt_expiry = Column(DateTime)
