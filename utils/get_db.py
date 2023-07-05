from utils.database import *

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()