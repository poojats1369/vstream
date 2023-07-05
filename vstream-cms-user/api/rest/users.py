import uuid
from api.db import *
from utils import *
from typing import List
from api.domain import *
from typing import Annotated
from datetime import timedelta
from api.helper.helper import *
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter, status, Query, Body

users_router = APIRouter()

expiry_time = 30

@users_router.post("/user")
def create_user(request: CmsBase, db: Session = Depends(get_db)):
    result = add_user(request, db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_CREATED_MSG"],# "User created successfully",
                    "type": "created",
                }],
                "is_data": is_data
            }
        }
    else:
        return {
            "response": {
                "code": common["SERVER_ERROR"],
                "status": "failure",
                "alert": [{
                    "message":common["SERVER_ERROR_MSG"],# "",
                    "type": "failure",
                }],
                "is_data": is_data
            }
        }

@users_router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)
):
    user = db.query(CmsUsers).filter(CmsUsers.email==form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        return False
    access_token_expires = timedelta(minutes=expiry_time)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    existing_token = db.query(Token).filter(Token.user_id==user.id).first()
    if existing_token:
        existing_token.access_token = access_token
    else:
        token = Token(
            id=uuid.uuid4().hex,
            access_token=access_token,
            user_id=user.id
        )
        db.add(token)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get("/user/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    result = get_user_by_id(user_id,db)
    is_data = 1 if result else 0
    if result:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_FETCHED_MSG"],# "User fetched successfully ",
                    "type": "Fetch"
                }],
                "data":result,
                "is_data":is_data                
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "failure",
                "alert": [{
                    "message":common["NO_USER_MESSAGE"],# "User not found",
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }
    
@users_router.get("/users")
def get_users(db: Session = Depends(get_db)):
    result=get_all_users(db)
    is_data = 1 if result else 0

    if result:
        user_list = []
        for user in result:
            user_data = {
                "id":user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "emp_id": user.emp_id,
                "password":user.password,
                "role": user.role,
                "phone": user.phone,
                "email_verified": user.email_verified,
                "phone_verified": user.phone_verified,
                "created_at":user.created_at,
                "updated_at":user.updated_at,
                "is_active": user.is_active
            }
            user_list.append(user_data)

        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
               "alert": [{
                    "message":common["SUCCESS_FETCHED_MSG"],# "Users fetched successfully ",
                    "type": "Fetch"                    
                }],
                "data":user_list,
                "is_data":is_data                 
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "failure",
                "alert": [{
                    "message":common["NO_USER_MESSAGE"],# "Users not found",
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }

@users_router.get('/send_otp')
def sendotp(email: str = Query(None), phone: str = Query(None), db: Session = Depends(get_db)):
    result = send_otp(email, phone, db)
    is_data = 1 if result['success'] else 0

    if result['success']:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["OTP_SUCCESS_MESSAGE"],# "Otp sent successfully",
                    "type": "generated"
                }],
                "data":{
                    "otp": result['otp']
                    },
                "is_data": is_data
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

@users_router.put("/verify_user")
def verify_user(user_otp: str, db: Session = Depends(get_db)):
    result = verifyuser(user_otp, db)
    if result["success"]:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_VERIFIED_MSG"],# "User successfully verified.",
                    "type": "Verify"
                }]
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
                }]
            }
        }

@users_router.put("/forgot_password")
def forgot_password(user_otp: str, new_password: str = Body(), confirm_password: str = Body(), db: Session = Depends(get_db)):
    result = forgot_pass(user_otp, new_password, confirm_password, db)
    if result["success"]:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_UPDATED_MSG"],# "Password updated successfully.",
                    "type": "update",
                }]
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
                }]
            }
        }

@users_router.delete("/users/{user_id}")
def del_user(user_id: str, token: Annotated[str, Depends(oauth2_scheme)], email: str = Body(), password: str = Body(), db: Session = Depends(get_db)):
    result = delete_user(user_id, email, password, db)
    if result:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["USER_DELETED"],# f"User deleted successfully.",
                    "type": "delete",
                }]
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "failure",
                "alert": [{
                    "message":common["NO_USER_MESSAGE"],# "User not found or invalid credentials",
                    "type": "failure"
                }],
            }
        }