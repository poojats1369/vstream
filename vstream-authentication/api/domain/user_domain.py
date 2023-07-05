import uuid, re
from api.db import *
from api.db.user_model import *
from utils import *
from api.helper import *
from sqlalchemy.orm import Session
from api.domain import *

# def register_user(account: UserBase, device: DeviceBase, db: Session):
#     CURRENT_TIME = get_current_time()  # Update the current time

#     fld_phone = False
#     fld_email = False
#     if account.phone_no:
#         fld_phone = check_unique(account.phone_no, None, db)
#         if len(account.phone_no) != 10 or not account.phone_no.isdigit():
#             return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['INVALID_PH_NO']}
#         if not fld_phone:
#             return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_PH_NO']}
    
#     if account.phone_no and account.phone_code is None:
#         return {"success": False, "code": common['NOT_FOUND'], "message": common['PHONE_CODE_REQUIRED']}

#     if account.first_name is None:
#             return {"success": False, "code": common['NOT_FOUND'], "message": common['NAME_ERROR']}

#     if account.email:
#         fld_email = check_unique(None, account.email, db)
#         if not re.match(EMAIL_REGEX, account.email):
#             return {"success": False, "code": common['INVALID_DATA'], "message": common['INVALID_EMAIL']}
#         if not fld_email:
#             return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_EMAIL']}
    
#     if account.phone_no and account.phone_code and account.email:
#         return{"success": False, "code": common['INVALID_DATA'], "message": common['DETAILS_REQUIRED']}

#     if fld_phone or fld_email:
#         user_id = uuid.uuid4().hex

#         # # Convert the gender value to the appropriate enum value
#         # gender_value = account.gender
#         # if account.gender:
#         #     gender_input = account.gender.lower()
#         #     if gender_input in [choice.value for choice in GenderEnum]:
#         #         gender_value = GenderEnum(gender_input)


#         #     elif account.gender and account.gender.lower() not in [choice.value for choice in GenderEnum]:
#         #         return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}

#         if account.gender.lower() not in ['male','female','other']:
#                 return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}


#         new_user = User(
#             user_id=user_id,
#             phone_no=account.phone_no if account.phone_no else None,
#             phone_code=account.phone_code if account.phone_code else None,
#             email=account.email if account.email else None,
#             first_name=account.first_name if account.first_name else None,
#             last_name=account.last_name if account.last_name else None,
#             date_of_birth=account.date_of_birth if account.date_of_birth else None,
#             # password=get_password_hash(account.password) if account.password else None,
#             social_id=account.social_id if account.social_id else None,
#             social_type=account.social_type if account.social_type else None,
#             app_language=account.app_language if account.app_language else None,
#             gender=account.gender.capitalize(),
#             profile_image=account.profile_image if account.profile_image else None,
#             bio=account.bio if account.bio else None,
#             longitude=account.longitude if account.longitude else None,
#             latitude=account.latitude if account.latitude else None,
#             created_at = CURRENT_TIME
#         )

#         db.add(new_user)
#         db.flush()

#         new_profile = UserProfile(
#             profile_id=uuid.uuid4().hex,  # Generate a unique profile ID
#             user_id=user_id,
#             profile_name=account.first_name,
#             profile_image=account.profile_image if account.profile_image else None,
#             content_language=[account.app_language] if account.app_language else None,
#             gender=account.gender.capitalize(),
#             created_at= CURRENT_TIME,
#             status=True  
#         )

#         db.add(new_profile)
#         db.commit()

#         new_device = Device(
#             user_id=user_id,
#             device_name=device.device_name if device.device_name else None,
#             device_type=device.device_type if device.device_type else None,
#             os=device.os if device.os else None,
#             os_version=device.os_version if device.os_version else None,
#             device_token=device.device_token if device.device_token else None,
#             app_version=device.app_version if device.app_version else None
#         )
#         db.add(new_device)
#         db.commit()

#         if fld_phone:
#             result_otp = send_otp(None, account.phone_no, user_id, db)
#         else:
#             result_otp = send_otp(account.email, None, user_id, db)

#         return {
#             "success": True,
#             "otp": result_otp["otp"]
#             # "access_token": access_token,
#             # "token_type": "bearer",
#         }
#     else:
#         return {"success": False, "message": common["DETAILS_REQUIRED"]}

def register_user(account: UserBase, device: DeviceBase, db: Session):
    CURRENT_TIME = get_current_time()  # Update the current time

    fld_phone = False
    fld_email = False
    if account.phone_no:
        fld_phone = check_unique(account.phone_no, None, db)
        if len(account.phone_no) != 10 or not account.phone_no.isdigit():
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['INVALID_PH_NO']}
        if not fld_phone:
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_PH_NO']}
    
    if account.phone_no and not account.phone_code:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['PHONE_CODE_REQUIRED']}

    if account.first_name is None:
            return {"success": False, "code": common['NOT_FOUND'], "message": common['NAME_ERROR']}

    if account.email:
        fld_email = check_unique(None, account.email, db)
        if not re.match(EMAIL_REGEX, account.email):
            return {"success": False, "code": common['INVALID_DATA'], "message": common['INVALID_EMAIL']}
        if not fld_email:
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['EXISTING_EMAIL']}
    
    if account.phone_no and account.phone_code and account.email:
        return{"success": False, "code": common['INVALID_DATA'], "message": common['DETAILS_REQUIRED']}

    if fld_phone or fld_email:
        user_id = uuid.uuid4().hex

        if account.gender.lower() not in ['male','female','other']:
                return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}

        new_user = User(
            user_id=user_id,
            phone_no=account.phone_no if account.phone_no else None,
            phone_code=account.phone_code if account.phone_code else None,
            email=account.email if account.email else None,
            first_name=account.first_name if account.first_name else None,
            last_name=account.last_name if account.last_name else None,
            date_of_birth=account.date_of_birth if account.date_of_birth else None,
            # password=get_password_hash(account.password) if account.password else None,
            social_id=account.social_id if account.social_id else None,
            social_type=account.social_type if account.social_type else None,
            app_language=account.app_language if account.app_language else None,
            gender=account.gender.capitalize(),
            profile_image=account.profile_image if account.profile_image else None,
            bio=account.bio if account.bio else None,
            longitude=account.longitude if account.longitude else None,
            latitude=account.latitude if account.latitude else None,
            created_at = CURRENT_TIME
        )

        db.add(new_user)
        db.flush()

        new_profile = UserProfile(
            profile_id=uuid.uuid4().hex,  # Generate a unique profile ID
            user_id=user_id,
            profile_name=account.first_name,
            profile_image=account.profile_image if account.profile_image else None,
            content_language=[account.app_language] if account.app_language else None,
            created_at= CURRENT_TIME,
            gender=account.gender.capitalize(),
            status=True  
        )

        db.add(new_profile)
        db.commit()

        new_device = Device(
            user_id=user_id,
            device_name=device.device_name if device.device_name else None,
            device_type=device.device_type if device.device_type else None,
            os=device.os if device.os else None,
            os_version=device.os_version if device.os_version else None,
            device_token=device.device_token if device.device_token else None,
            app_version=device.app_version if device.app_version else None
        )
        db.add(new_device)
        db.commit()

        if fld_phone:
            result_otp = send_otp(None, account.phone_no,account.phone_code, user_id, db)
        else:
            result_otp = send_otp(account.email, None, None, user_id, db)

        return {
            "success": True,
            "otp": result_otp["otp"]
            # "access_token": access_token,
            # "token_type": "bearer",
        }
    else:
        return {"success": False, "message": common["DETAILS_REQUIRED"]}



def user_login(data: LoginBase, db: Session):
    CURRENT_TIME = get_current_time()  # Update the current time

    if data.phone_no and not data.phone_code:
        return {"success": False, "code": common['FAILURE'], "message": common['PHONE_CODE_REQUIRED']}

    if data.phone_no and data.email:
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
    expiry_time = current_time + timedelta(minutes=OTP_EXPIRE_TIME)
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
    # access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME)
    # access_token = create_access_token(
    #     data={"user_id": user.user_id}, expires_delta=access_token_expires
    #     )
    # existing_token = db.query(Token).filter(Token.user_id==user.user_id).first()
    # if existing_token:
    #     existing_token.access_token = access_token
    # else:
    #     token = Token(
    #         access_token=access_token,
    #         user_id=user.user_id
    #     )
    #     db.add(token)
    # db.commit()
    # return {"success": True, "access_token": access_token, 'otp': otp, "token_type": "bearer"}
    return {"success": True, 'otp': otp}

def logout_user(token, db):

    CURRENT_TIME = get_current_time()  # Update the current time
    
    token_record = db.query(Token).filter(Token.access_token == token).first()

    if token_record and CURRENT_TIME >= token_record.rt_expiry:
        return {"success": False, "code": common['FORBIDDEN'], "message": common['RT_EXPIRED']}


    if not token_record:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}

    user_id = token_record.user_id  # Retrieve the user_id from the token record
    db.query(Token).filter(Token.user_id == user_id).delete()

    db.commit()

    return {"success": True, "message": common['USER_LOGOUT']}


