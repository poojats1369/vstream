import random
from api.db import *
from utils import *
from datetime import  timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

# Load the .env file
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def check_unique(phone_no, email_id, db):
    if phone_no!=None:
        phone = db.query(User).filter(User.phone_no == phone_no).first()
        if phone:
            return False
        
    if email_id!=None:
        email = db.query(User).filter(User.email == email_id).first()
        if email:
            return False    
    return True


def send_otp(email, phone_no,phone_code, user_id,db: Session):
    CURRENT_TIME = get_current_time()
    if not email and not phone_no:
        # message = "Please provide email or phone number"
        code = 400
        return {"success": False, "code": common['FAILURE'], "message": common['DETAILS_REQUIRED']}
    
    otp = random.randint(OTP_START_RANGE, OTP_END_RANGE)

    current_time = CURRENT_TIME
    expiry_time = current_time + timedelta(minutes=OTP_EXPIRE_TIME)

    otp_user = Otp(
        user_id=user_id,
        phone_no=phone_no  if phone_no else None,
        phone_code=phone_code  if phone_code else None,
        email=email if email else None,
        otp_code=otp,
        expiry_datetime=expiry_time,
        no_of_attempts=1
    )
    db.add(otp_user)
    db.commit()

    if otp:
        return {
            'success': True,
            'otp': otp
        }
    else:
        False

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_data(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_no": user.phone_no,
        "phone_code": user.phone_code,
        "email_verified": user.email_verified,
        "phone_verified": user.phone_verified,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "social_id": user.social_id,
        "social_type": user.social_type,
        "bio": user.bio,
        "app_language": user.app_language
    }

def get_user_profiles(profile: UserProfileSchemaForGet):
    return {
        "profile_name": profile.profile_name,
        "profile_image": profile.profile_image,
        "date_of_birth": profile.date_of_birth,
        "gender": profile.gender,
        "content_language": profile.content_language,
        "genre": profile.genre,
        "is_child": profile.is_child,
        "status": profile.status
    }


