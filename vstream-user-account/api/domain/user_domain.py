import re
from api.db import *
from utils import *
from api.helper import *
from utils import *
from sqlalchemy.orm import Session

def user_update(token: str, account: UpdateUserBase, device_data: UpdateDeviceBase, db: Session):
    CURRENT_TIME = get_current_time()  
    fld_phone = False
    fld_email = False

    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()
    device = db.query(Device).filter(Device.user_id == user.user_id).first()
    otp = db.query(Otp).filter(Otp.user_id == user.user_id).first()
    if not user:
        return {"success": False, "code": common['NOT_FOUND'],  "message": common['NO_USER_MESSAGE']}

    if user_token and CURRENT_TIME >= user_token.rt_expiry:
        return {"success": False, "code": common['FORBIDDEN'], "message": common['RT_EXPIRED']}

    if account.phone_no:
        if len(account.phone_no) != 10 or not account.phone_no.isdigit():
            return {"success": False, "code": common['FAILURE'], "message": common['INVALID_PH_NO']}
        elif user.phone_no:
            return {"success": False, "code": common['FAILURE'], "message": common['PHONE_NO_EXISTS_ERROR']}
        elif not account.phone_code:
            return {"success": False, "code": common['FAILURE'], "message": common['INVALID_PH_CODE']}
   
    if account.phone_code and not account.phone_no:
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_PH_NO']}
    
    if account.email:    
        if not re.match(EMAIL_REGEX, account.email):
            return {"success": False, "code": common['FAILURE'], "message": common['INVALID_EMAIL']}
        elif user.email:
            return {"success": False, "code": common['FAILURE'], "message": common['EMAIL_EXISTS_ERROR']}

    if account.phone_no:
        fld_phone = check_unique(account.phone_no, None, db)
        if not fld_phone:
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_PH_NO']}

    if account.email:
        fld_email = check_unique(None, account.email, db)
        if not fld_email:
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_EMAIL']}

    if account.gender and account.gender.lower() not in ['male', 'female', 'other']:
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}

    user.first_name = account.first_name if account.first_name else user.first_name
    user.last_name = account.last_name if account.last_name else user.last_name
    user.date_of_birth = account.date_of_birth if account.date_of_birth else user.date_of_birth

    if account.email and not user.email:
        user.email = account.email

    if account.phone_no and not user.phone_no:
        user.phone_no = account.phone_no

    if account.phone_code and not user.phone_code:
        user.phone_code = account.phone_code

    user.gender = account.gender.capitalize() if account.gender else user.gender
    user.profile_image = account.profile_image if account.profile_image else user.profile_image
    user.bio = account.bio if account.bio else user.bio
    user.longitude = account.longitude if account.longitude else user.longitude
    user.latitude = account.latitude if account.latitude else user.latitude
    user.updated_at = CURRENT_TIME
    db.add(user)

    device.device_token = device_data.device_token if device_data.device_token else device.device_token
    device.app_version = device_data.app_version if device_data.app_version else device.app_version
    db.add(device)

    otp.phone_no = account.phone_no if account.phone_no else otp.phone_no
    otp.phone_code = account.phone_code if account.phone_code else otp.phone_code
    otp.email = account.email if account.email else otp.email
    db.add(otp)

    db.commit()

    updated_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_no": user.phone_no,
        "phone_code": user.phone_code,
        "email_verified": user.email_verified,
        "phone_verified": user.phone_verified,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "bio": user.bio
    }
    return updated_data


def get_user_loggedin(token:str, db:Session):

    CURRENT_TIME = get_current_time()  # Update the current time

    user_token = db.query(Token).filter(Token.access_token == token).first()

    profiles = db.query(UserProfile).filter(UserProfile.user_id==user_token.user_id).all()
    user_profiles = []
    for profile in profiles:
        user_profiles.append(get_user_profiles(profile))

    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    if CURRENT_TIME >= user_token.rt_expiry:
        return {"success": False, "code": common['FORBIDDEN'], "message": common['RT_EXPIRED']}

    else:
        user = db.query(User).filter(User.user_id == user_token.user_id).first()
        if not user:
            return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}
        else:
            user_data = get_user_data(user)
            return {"success": True, **user_data, "profiles":user_profiles}

def delete_user(token: str, db: Session):
   
    CURRENT_TIME = get_current_time()  # Update the current time

    # Retrieve the token entry from the Tokens table
    token_entry = db.query(Token).filter(Token.access_token == token).first()
    
    if token_entry and CURRENT_TIME >= token_entry.rt_expiry:
        return {"success": False, "code": common['FORBIDDEN'], "message": common['RT_EXPIRED']}

    if token_entry:
        user_id = token_entry.user_id

        # Delete the OTP records associated with the user
        db.query(Otp).filter(Otp.user_id == user_id).delete()

        # Delete the user profile
        db.query(UserProfile).filter(UserProfile.user_id == user_id).delete()

        # Delete the user's devices
        db.query(Device).filter(Device.user_id == user_id).delete()

        # Delete the token
        db.query(Token).filter(Token.access_token == token).delete()

        # Delete the user
        db.query(User).filter(User.user_id == user_id).delete()

        db.commit()

        return {"success": True}
    else:
        return {"success": False}


