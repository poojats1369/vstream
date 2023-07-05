from api.db import *
from utils import *
from api.helper import *
from utils import *

def retrieve_intro_screen_data(db:Session):
    intro_screen = db.query(IntroScreen).all()
    screen_count = len(intro_screen)
    if intro_screen:
        return{"success":True,"data":{"no_of_screen":screen_count,"screens":intro_screen},}
    return{"success":False}
