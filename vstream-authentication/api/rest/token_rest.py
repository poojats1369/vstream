from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

token_router = APIRouter(prefix="/v1")

@token_router.post("/refresh-token")
def refresh_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
    result = refresh_token_fun(refresh_token, db)
    is_data = 1 if result['success'] else 0
    if result["success"]:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "created"
                }],
                "is_data": is_data,
                  "data":{
                    "access_token": result["access_token"],
                    "at_expiry": result["at_expiry"],
                    "expires_in": result["expires_in"]
                }
            }
        }
    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure"
                }],
                "is_data": is_data
            }
        }

