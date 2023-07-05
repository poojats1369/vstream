from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


introscreen_router = APIRouter(prefix="/v1")

@introscreen_router.get("/intro-screen")
def intro_screen(db: Session = Depends(get_db)):
    result = retrieve_intro_screen_data(db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "success",
                }],
                "is_data": is_data,
                "data": result["data"]
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": common['NO_CONTENT_MSG'],
                    "type": "failure",
                }],
                "is_data": is_data
            }
        }
    
    