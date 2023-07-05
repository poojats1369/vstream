import uuid, re
from datetime import datetime
from utils import *
from api.db import *
from sqlalchemy.orm import Session
from api.helper.helper import *


def add_user(request: CmsBase, db: Session):
    valid_roles = ["super_admin", "admin", "editor", "author", "subscriber"]
    lower_case_role = request.role.lower()
    if lower_case_role not in valid_roles:
        message = """Invalid role. Your role can be "super_admin", "admin", "editor", "author", "subscriber" """
        code = 400
        return {"success": False, "code": code, "message": message}

    if request.role.lower() == "super_admin" and db.query(CmsUsers).filter(CmsUsers.role == "super_admin").first():
        message = "Super admin already exists."
        code = 409
        return {"success": False, "code": code, "message": message}

    fld_unique = check_unique(request.phone, request.email, request.emp_id, db)
    if not fld_unique:
        message = "email | phone no | emp_id already exists."
        code = 409
        return {"success": False, "code": code, "message": message}

    if len(request.phone) != 10 or not request.phone.isdigit():
        message = "Invalid phone number format, please enter 10 digits."
        code = 409
        return {"success": False, "code": code, "message": message}
    
    if not re.match(regex, request.email):
        message = "Invalid email format."
        code = 400
        return {"success": False, "code": code, "message": message}

    if fld_unique:
        db_user = CmsUsers(
            id=uuid.uuid4().hex,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            emp_id=request.emp_id,
            password=get_password_hash(request.password),
            role=request.role.lower(),
            phone=request.phone
        )
        db.add(db_user)
        db.commit()

        return {"success": True}
    else:
        return {"success": False}

def get_user_by_id(user_id:str,db:Session):
    user = db.query(CmsUsers).filter(CmsUsers.id == user_id).first()
    return user

def get_all_users(db:Session):
    users =  db.query(CmsUsers).all()
    if users:
        return users
    else:
        False
  
def delete_user(user_id: str, email: str, password: str, db: Session):
    user = db.query(CmsUsers).get(user_id)
    if user:
        if user.email == email and verify_password(password, user.password):
            delete_token = db.query(Token).filter(Token.user_id == user_id).first()
            if delete_token:
                db.delete(delete_token)
            db.delete(user)
            
            otp_user = db.query(OtpTable).filter(OtpTable.user_id == user_id).first()
            if otp_user:
                db.delete(otp_user)
            
            db.commit()
            return True
    return False

def verifyuser(user_otp: str, db: Session):
    otpuser = db.query(OtpTable).filter(OtpTable.otp_code==user_otp).first()
    if otpuser is None:
        message = "Invalid OTP code."
        code = 400
        return {"success": False, "code": code, "message": message}
    user = db.query(CmsUsers).filter(CmsUsers.id==otpuser.user_id).first()
    if datetime.now() >= otpuser.expiry_date:
        otpuser.is_expired=True
        db.add(otpuser)
        db.commit()
        message = "Your OTP has expired."
        code = 400
        return {"success": False, "code": code, "message": message}
    if user:
        user.email_verified=True
        user.phone_verified=True
        db.add(user)
        db.commit()
        return {"success": True}
    return {"success": False, "code": 400, "message": "User not found."}

def forgot_pass(user_otp: str, new_password: str, confirm_password: str, db: Session):
    otpuser = db.query(OtpTable).filter(OtpTable.otp_code == user_otp).first()

    if otpuser is None:
        message = "Invalid OTP code."
        code = 400
        return {"success": False, "code": code, "message": message}

    if datetime.now() >= otpuser.expiry_date:
        otpuser.is_expired = True
        db.add(otpuser)
        db.commit()
        message = "Your OTP has expired."
        code = 400
        return {"success": False, "code": code, "message": message}

    user = db.query(CmsUsers).filter(CmsUsers.id == otpuser.user_id).first()
    if user:
        if new_password != confirm_password:
            message = "Passwords do not match."
            code = 400
            return {"success": False, "code": code, "message": message}

        user.password = get_password_hash(new_password)
        db.add(user)
        db.commit()
        return {"success": True}

    return {"success": False, "code": 400, "message": "User not found."}

def update_single_user(user_id: str, single_user_data: CmsUpdate, db: Session):
    user = db.query(CmsUsers).filter(CmsUsers.id == user_id).first()
    if not user:
        message = "User not found"
        code = 404
        return {"success": False, "code": code, "message": message}

    is_unique = check_unique_02(single_user_data.phone, single_user_data.email, db)
    if not is_unique:
        message = "Phone number or email is not unique"
        code = 400
        return {"success": False, "code": code, "message": message}

    valid_roles = ["super_admin", "admin", "editor", "author", "subscriber"]
    if single_user_data.role.lower() not in valid_roles:
        message = "Invalid role"
        code = 400
        return {"success": False, "code": code, "message": message}

    if single_user_data.role.lower() == "super_admin" and db.query(CmsUsers).filter(CmsUsers.role == "super_admin").first():
        message = "Super admin already exists."
        code = 409
        return {"success": False, "code": code, "message": message}

    if len(single_user_data.phone) != 10 or not single_user_data.phone.isdigit():
        message = "Invalid phone number format, please enter 10 digits."
        code = 409
        return {"success": False, "code": code, "message": message}
    
    if not re.match(regex, single_user_data.email):
        message = "Invalid email format."
        code = 400
        return {"success": False, "code": code, "message": message}

    user_otp = db.query(OtpTable).filter(user.id == OtpTable
                                         .user_id).first()

    if user_otp:
        user_otp.phone_number = single_user_data.phone
        user_otp.email = single_user_data.email
        db.commit()

    user.first_name = single_user_data.first_name
    user.last_name = single_user_data.last_name
    user.email = single_user_data.email
    user.emp_id = single_user_data.emp_id
    user.phone = single_user_data.phone
    user.role = single_user_data.role.lower()
    db.add(user)
    db.commit()

    updated_user = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "emp_id": user.emp_id,
        "phone": user.phone,
        "role": user.role
    }
    
    return updated_user

def update_multiple_users(multiple_users_data: List[UpdateStatusSchema], db: Session):
    for user_data in multiple_users_data:
        user = db.query(CmsUsers).filter_by(id=user_data.user_id).first()
        if not user:
            message = "User not found"
            code = 404
            return {"success": False, "code": code, "message": message}
        valid_roles = ["super_admin", "admin", "editor", "author", "subscriber"]
        if user_data.role.lower() not in [role.lower() for role in valid_roles]:
            message = "Invalid role"
            code = 400
            return {"success": False, "code": code, "message": message}

        if user_data.role.lower() == "super_admin" and db.query(CmsUsers).filter(CmsUsers.role == "super_admin").first():
            message = "Super admin already exists or there can be only one super admin."
            code = 409
            return {"success": False, "code": code, "message": message}

        user.is_active = user_data.is_active
        user.role = user_data.role.lower()
        db.add(user)
        db.commit()
    return {"success": True}

