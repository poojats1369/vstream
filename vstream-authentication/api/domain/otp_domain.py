import uuid
from utils import *
from api.db import *
from api.helper import *
from sqlalchemy.orm import Session


def otp_send(data: LoginBase, db: Session):
    
    CURRENT_TIME = get_current_time()  # Update the current time

    if data.phone_no and not data.phone_code:
        return {"success": False, "code": common['FAILURE'], "message": common['PHONE_CODE_REQUIRED']}

    if (data.phone_no or data.phone_code) and data.email:
        return {"success": False, "code": common['FAILURE'], "message": common['ANY_ONE_DETAIL_REQUIRED']}
    
    if data.phone_no is None and data.email is None:
        return {"success": False, "code": common['FAILURE'], "message": common['DETAILS_REQUIRED']}
  
    user = None
    if data.email:
        user = db.query(User).filter_by(email=data.email).first()
    else:
        user = db.query(User).filter_by(phone_no=data.phone_no).first()

    if not user:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}

    otp = random.randint(OTP_START_RANGE, OTP_END_RANGE)
    otp_user = db.query(Otp).filter(Otp.user_id == user.user_id).first()

    current_time = CURRENT_TIME
    expiry_time = current_time + timedelta(minutes=15)

    if otp_user is None:
        otp_user = Otp(
            id=uuid.uuid4().hex,
            user_id=user.user_id,
            phone_code=user.phone_code,
            phone_no=user.phone_no,
            email=user.email,
            otp_code=otp,
            expiry_datetime=expiry_time,
            no_of_attempts=1
        )
        db.add(otp_user)
    else:
        otp_user.phone_code = user.phone_code
        otp_user.otp_code = otp
        otp_user.expiry_datetime = expiry_time
        otp_user.no_of_attempts += 1
        otp_user.is_expired = False
    db.commit()

    return {"success": True,  'otp': otp}

def verify_otp(data: str, db: Session):
    CURRENT_TIME = get_current_time()  # Update the current time

    if not ((data.user_otp and data.phone_no and data.phone_code) or (data.user_otp and data.email)):
        return {
            "success": False,
            "code": common['FAILURE'],
            "message": common['DETAILS_REQUIRED']
        }

    if len(data.user_otp) != 4 or not data.user_otp.isdigit():
        return {"success": False, "code": common['NOT_FOUND'], "message": common['INVALID_OTP']}

    otpuser = db.query(Otp).filter(Otp.otp_code == data.user_otp).first()
    if otpuser is None:
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_OTP']}

    user = db.query(User).filter(User.user_id == otpuser.user_id).first()

    if CURRENT_TIME >= otpuser.expiry_datetime:
        otpuser.is_expired = True
        db.add(otpuser)
        db.flush()
        return {"success": False, "code": common['FAILURE'], "message": common['EXPIRED_OTP']}

    # Check if phone number and phone code belong to the same user
    if data.phone_no and data.phone_code and (user.phone_no != data.phone_no or user.phone_code != data.phone_code):
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_DETAILS']}

    # Check if email and OTP belong to the same user.
    if data.email and (user.email != data.email):
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_DETAILS']}

    # Update phone_verified or email_verified based on the data
    if data.phone_no:
        user.phone_verified = True
    elif data.email:
        user.email_verified = True
    else:
        user.phone_verified = True
        user.email_verified = True

    # Generate access token
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME)
    access_token = create_access_token(
        data={"user_id": user.user_id}, expires_delta=access_token_expires
    )

    # Generate refresh token
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_TIME)
    refresh_token = create_access_token(
        data={"user_id": user.user_id}, expires_delta=refresh_token_expires
    )

    # Update last_login_datetime
    user.last_login_datetime = CURRENT_TIME
    db.add(user)
    db.commit()

    existing_token = db.query(Token).filter(Token.user_id == user.user_id).first()
    if existing_token:
        existing_token.access_token = access_token
        existing_token.at_created = CURRENT_TIME
        existing_token.at_expiry = CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME)
        existing_token.refresh_token = refresh_token
        existing_token.rt_created = CURRENT_TIME
        existing_token.rt_expiry = CURRENT_TIME + timedelta(days=REFRESH_TOKEN_EXPIRE_TIME)
    else:
        token = Token(
            user_id=user.user_id,
            access_token=access_token,
            at_created=CURRENT_TIME,
            at_expiry=CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME),
            refresh_token=refresh_token,
            rt_created=CURRENT_TIME,
            rt_expiry=CURRENT_TIME + timedelta(days=REFRESH_TOKEN_EXPIRE_TIME)
        )
        db.add(token)
    db.commit()

    expiry_time_at = (CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME))
    formatted_expiry_at = expiry_time_at.strftime("%Y-%m-%d %H:%M:%S")
    expiry_time_rt = (CURRENT_TIME + timedelta(days=REFRESH_TOKEN_EXPIRE_TIME))
    formatted_expiry_rt = expiry_time_at.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "success": True,
        "access_token": access_token,
        "at_expiry": formatted_expiry_at,
        "at_expires_in": f"{ACCESS_TOKEN_EXPIRE_TIME} hrs ",
        "refresh_token": refresh_token,
        "rt_expiry": formatted_expiry_rt,
        "rt_expires_in": f"{REFRESH_TOKEN_EXPIRE_TIME} days "
    }
