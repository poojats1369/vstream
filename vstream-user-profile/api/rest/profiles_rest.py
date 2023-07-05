from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

profiles_router = APIRouter(prefix="/v1")

@profiles_router.post("/profiles")
def create_profile(user_profile: UserProfileSchema,token: str=Header(), db: Session = Depends(get_db)):
    result = register_profile(token, user_profile, db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": 201,
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "created",
                }],
                "is_data": is_data,
                "data":result['details']
            }
        }
    else:
        return {
            "response": {
                "code": 500,
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                "is_data": is_data
            }
        }

@profiles_router.get('/profiles')
def get_profiles(token: str=Header(), db: Session = Depends(get_db)):
    result = get_profiles_logged_in(token, db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"
                }],
                "is_data":is_data,                
                "data":result['details']
            }
        }
    else:
        return {
            "response": {
                "code": 404,
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }
    
@profiles_router.get("/profile")
def get_profile(profile_id: str, token: str=Header(),  db: Session = Depends(get_db)):
    result = get_profile_by_id(token, profile_id, db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"
                }],
                "is_data":is_data,                
                "data":result['details']
            }
        }
    else:
        return {
            "response": {
                "code": 404,
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }
    
@profiles_router.delete("/profiles")
def delete_profile(profile_id: str, token: str=Header(),  db: Session = Depends(get_db)):
    result = profile_delete(token, profile_id, db)
    if result['success']:
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": common['USER_DELETED'],
                    "type": "delete",
                }]
            }
        }
    else:
        return {
            "response": {
                "code": 404,
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
            }
        }
    
@profiles_router.put("/profiles")
def update_profile(user_profile: UserProfileIDSchema,token: str=Header(), db: Session = Depends(get_db)):
    result = profiles_update(token, user_profile, db) 
    is_data = 1 if result['success'] else 0 
    if result["success"]:
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_UPDATED_MSG'],
                    "type": "Update"
                }],
                "is_data": is_data,
                "data": result['details']
            }
        }
    else:
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
    
