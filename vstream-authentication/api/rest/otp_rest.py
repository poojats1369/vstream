from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

otp_router = APIRouter(prefix="/v1")

@otp_router.post('/send-otp')
def send_otp(phone_or_email: LoginBase , db: Session = Depends(get_db)):
    result = otp_send(phone_or_email, db)
    is_data = 1 if result['success'] else 0

    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['OTP_SUCCESS_MESSAGE'],
                    "type": "success"
                }],
                "is_data": is_data,
                # "data":{
                #     "otp": result['otp']
                #     },
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
                "is_data": is_data
            }
        }

@otp_router.post("/otp-verify")
def otp_verify(user_otp: OtpBase, db: Session = Depends(get_db)):
    result = verify_otp(user_otp, db)
    is_data = 1 if result['success'] else 0
    if result["success"]:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_VERIFIED_MSG'],
                    "type": "Verify"
                }],
                "is_data": is_data,
                  "data":{
                    "access_token": result["access_token"],
                    "at_expiry": result["at_expiry"],
                    "at_expires_in": result["at_expires_in"],
                    "refresh_token": result["refresh_token"],
                    "rt_expiry": result["rt_expiry"],
                    "rt_expires_in": result["rt_expires_in"],
                    "auto_login":"true"
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
