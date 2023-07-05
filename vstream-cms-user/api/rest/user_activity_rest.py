from api.db import *
from api.domain import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Body
from utils import *

user_activity_router = APIRouter()


@user_activity_router.post("/user-activity")
def user_activity(request_1: UserActivityLogSchema, request_2: UserActivityListSchema, db: Session = Depends(get_db)):
    result = user_activity_funct(request_1, request_2, db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "Created"
                }],
                "is_data": is_data
            }
        }
    else:
        return {
            "response": {
                "code": common['FAILURE'],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure"
                }],
                "is_data": is_data
            }
        }


@user_activity_router.get("/user-activity/{activity_id}")
def get_user_activities(activity_id: str, db: Session = Depends(get_db)):
    result = get_user_by_activity_id(activity_id,db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Retrieved"
                }],
                "is_data": is_data,
                "data": result["activity"]
            }
        }
    else:
        return {
            "response": {
                "code": common['FAILURE'],
                "status": "failure",
                "alert": [{
                    "message": common['NO_PROFILE_MESSAGE'],
                    "type": "failure"
                }],
                "is_data": is_data
            }
        }

@user_activity_router.get("/user-activities")
def get_all_user_activities(db: Session = Depends(get_db)):
    result = get_all_user_activity(db)
    is_data = 1 if result['success'] else 0
    if result['success']:

        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Retrieved"
                }],
                "is_data": is_data,
                "data":  result["activities"]
            }
        }
    else:
        return {
            "response": {
                "code": common['FAILURE'],
                "status": "failure",
                "alert": [{
                    "message": common['NO_PROFILE_MESSAGE'],
                    "type": "failure"
                }],
                "is_data": is_data
            }
        }


