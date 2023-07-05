from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

users_router = APIRouter(prefix="/v1")

@users_router.put("/user")
def update_user(account: UpdateUserBase, device: UpdateDeviceBase, token: str = Header(), db: Session = Depends(get_db)):
    result = user_update(token, account, device, db) 
    is_data = 1 if result else 0 
    if "code" in result and "message" in result:
        return {
            "response": {
                "code": result["code"],
                "status": "Failure",
                "alert": [{
                    "message": result["message"],
                    "type": "Failure"
                }],
                "is_data": 0
            }
        }

    else:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_UPDATED_MSG'],
                    "type": "Update"
                }],
                "is_data": is_data,
                "data": result
            }
        }

@users_router.get("/user")
def get_user(token: str = Header(), db: Session = Depends(get_db)):
    result = get_user_loggedin(token,db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        result.pop('success')
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"
                }],
                "is_data":is_data,
                "data":result
                    }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data":is_data
            }
        }

@users_router.delete("/user")
def user_delete(token: str = Header(), db: Session = Depends(get_db)):
    result = delete_user(token, db)
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['USER_DELETED'],
                    "type": "success",
                }]
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": common['NO_USER_MESSAGE'],
                    "type": "failure"
                }],
            }
        }
    

