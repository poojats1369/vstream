import random, pytz, uuid, smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from utils import *
from api.db import *
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()
# Access the private constants
secret_key = os.environ.get('SECRET_KEY')
algo = os.environ.get('ALGORITHM')



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algo)
    return encoded_jwt

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def check_unique(phoneno, emailid, empid, db):
    phone = db.query(CmsUsers).filter(CmsUsers.phone == phoneno).first()
    email = db.query(CmsUsers).filter(CmsUsers.email == emailid).first()
    emp_id = db.query(CmsUsers).filter(CmsUsers.emp_id == empid).first()
    if phone or email or emp_id:
        return False
    return True

def check_unique_02(phone_no, email_id, db):
    phone = db.query(CmsUsers).filter(CmsUsers.phone == phone_no).first()
    email = db.query(CmsUsers).filter(CmsUsers.email == email_id).first()
    if phone or email:
        return False
    return True

def send_otp(email: str, phone: str, db: Session):
    if email is None and phone is None:
        message = "Please provide email or phone number"
        code = 400
        return {"success": False, "code": code, "message": message}
    user = None
    if email:
        user = db.query(CmsUsers).filter_by(email=email).first()
    elif phone:
        user = db.query(CmsUsers).filter_by(phone=phone).first()

    if not user:
        message = "User not found"
        code = 404
        return {"success": False, "code": code, "message": message}

    otp = random.randint(OTP_START_RANGE, OTP_END_RANGE)
    otp_user = db.query(OtpTable).filter(OtpTable.user_id == user.id).first()

    current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
    expiry_time = current_time + timedelta(minutes=15)

    if otp_user is None:
        otp_user = OtpTable(
            id=uuid.uuid4().hex,
            user_id=user.id,
            phone_code=user.phone_code,
            phone_number=user.phone,
            email=user.email,
            otp_code=otp,
            expiry_date=expiry_time,
            no_of_attempts=1
        )
        db.add(otp_user)
    else:
        otp_user.phone_code = user.phone_code
        otp_user.otp_code = otp
        otp_user.expiry_date = expiry_time
        otp_user.no_of_attempts += 1
        otp_user.is_expired = False
    db.commit()

    send_email("Email verification OTP", str(otp), "nicemltstng@outlook.com", user.email)
    if otp:
        return {
            'success': True,
            'otp': otp
        }
    else:
        False

def send_email(subject: str,body: str,sender_email: str,recipient_email: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login("nicemltstng@outlook.com", "Valtech123")
            server.send_message(msg)
    except Exception as e:
        return {"message": "Failed to send email", "error": str(e)}
    
    return {"message": "Email sent successfully"}