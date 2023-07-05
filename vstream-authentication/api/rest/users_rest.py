from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

users_router = APIRouter(prefix="/v1")

@users_router.post("/user")
def user_registration(account: UserBase, device: DeviceBase, db: Session = Depends(get_db)):
    result = register_user(account, device, db)
    # is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "success",
                }],
                "is_data": 0
                # "data": {
                #     "otp": result["otp"]
                #     # "access_token": result["access_token"]
                # },
            }
        }
    else:
        return {
            "response": {
                "code": common['FAILURE'],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                "is_data": 0
            }
        }

@users_router.post('/login')
def login(phone_or_email: LoginBase , db: Session = Depends(get_db)):
    result = user_login(phone_or_email, db)
    # is_data = 1 if result['success'] else 0

    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                     "message": common['OTP_SUCCESS_MESSAGE'],
                    "type": "generated"
                }],
                "is_data": 0,
                # "data":{
                #     "otp": result['otp']
                    # "access_token": result["access_token"]
                    # },
            }
        }
    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                "is_data": 0
            }
        }

@users_router.post("/logout")
def user_logout(token: str = Header(), db: Session = Depends(get_db)):
    result = logout_user(token, db)
    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['USER_LOGOUT'],
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
                    "message": result['message'],
                    "type": "failure"
                }],
            }
        }


