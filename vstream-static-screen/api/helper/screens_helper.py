import os
from api.db import *
from utils import *
from utils import *
from dotenv import load_dotenv

# Access the private constants
load_dotenv()

# def dbaccess():
#     mydb = mymongo[os.environ.get('POSTGRES_DB')]
#     return mydb 

# def intro_data_collection():  
#     db=dbaccess()
#     introData=db[os.environ.get('MONGODB_INTROSCREEN_COLLECTION')]
#     if introData!=None:
#         return introData
#     else:
#         return {"success":False}
