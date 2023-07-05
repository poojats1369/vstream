
from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from fastapi import  APIRouter

splash_router = APIRouter(prefix="/v1")

@splash_router.get("/splash-screen")
def splash_screen():
    result = retrieve_splash_screen_data()
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
                "data":{
                    "background_image": result["path"]
                },
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": common['SERVER_ERROR_MSG'],
                    "type": "failure",
                }],
                "is_data": is_data
            }
        }
