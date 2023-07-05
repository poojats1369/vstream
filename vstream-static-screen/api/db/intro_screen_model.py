from utils import *
from sqlalchemy import Column, Integer, String, ARRAY, Text

class IntroScreen(Base):
    __tablename__ = "intro_screen"

    id = Column(Integer, primary_key=True,autoincrement=True)
    screen_id = Column(Integer)
    background_image = Column(Text)
    title = Column(String)
    description = Column(String)
    logo = Column(Text)
    actions = Column(ARRAY(Text))
