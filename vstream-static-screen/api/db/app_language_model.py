from utils import *
from sqlalchemy import Column, Integer, String, Boolean, Text

class AppLanguage(Base):
    __tablename__ = "app_languages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language_code = Column(String)
    language_name = Column(String)
    language_text = Column(String)
    language_icon = Column(Text)
    status = Column(Boolean)