from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_TIME = 24  #in hours
REFRESH_TOKEN_EXPIRE_TIME = 180 #in days
OTP_EXPIRE_TIME = 15 #in mins

OTP_START_RANGE = 1000
OTP_END_RANGE = 9999

SPLASH_SCREEN_PATH = "D:/OTT/user/media/splash_screen.gif" 

EMAIL_REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]com$'

SECRET_KET = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')

# PORT = os.environ.get('PORT')

common = {
    'SUCCESS': 200,
    'NO_CONTENT': 204,
    'FORBIDDEN': 403,
    'SUCCESS_CREATED': 201,
    'FAILURE': 400,
    'INVALID_DATA': 400,
    'UNAUTHORIZED': 401,
    'NOT_FOUND':404,
    'ALREADY_EXISTING': 409,
    'SERVER_ERROR': 500,
    'SUCCESS_MSG': 'Success',
    'FAILURE_MSG': 'Failure',
    'LOGIN_SUCCESS': 'Login Success',
    'LOGIN_FAILED': 'Invalid Email/Password',
    'UNAUTHORIZED_MSG': 'Unauthorized',
    'APP_TOKEN_MISSING': 'Provide Application Token',
    'INVALID_EMAIL': 'Invalid Email',
    'INVALID_PASSWORD': 'Invalid Password',
    'INVALID_PARAM': 'Invalid Parameters',
    'ALREADY_EXISTING_MSG': 'Already Existing',
    'SUCCESS_ALERT': 'success',
    'FAILURE_ALERT': 'failure',

    'RT_EXPIRED':'Session expired',
    'NO_CONTENT_MSG': 'No Content',
    'INVALID_PH_NO' : "Invalid phone number format, please enter 10 digits.",
    'INVALID_EMAIL' : "Invalid email format.",
    'EXISTING_PH_NO' : "phone no already exists.",
    'EXISTING_EMAIL' : "Email Id already exists.",
    'EXPIRED_OTP' : "Your OTP has expired..",
    'INVALID_OTP' : "Invalid OTP code.",
    'INVALID_DETAILS' : "OTP does not match with your details",
    'INVALID_GENDER' : "Invalid Gender",
    'DETAILS_REQUIRED' : "Please provide email or phone number",
    'INVALID_PHONE_CODE':"Please enter valid phone code",
    'NO_USER_MESSAGE' : "User not found",
    "NOT_AUTH":"Not authenticated.",
    'OTP_SUCCESS_MESSAGE': 'Otp sent successfully',
    'SERVER_ERROR_MSG': 'Internal Server Error',
    'SUCCESS_CREATED_MSG': 'Successfully Created',
    'SUCCESS_FETCHED_MSG': 'Successfully Fetched',
    'SUCCESS_VERIFIED_MSG': 'Successfully Verified',
    'SUCCESS_UPDATED_MSG': 'Successfully Updated',
    'USER_NOT_DELETED' : "user not found or invalid credentials",
    'USER_DELETED' : "Successfully deleted",
    'USER_LOGOUT' : "Successfully Logged out",
    'PHONE_CODE_REQUIRED':"Enter the phone code",
    'PHONE_NO_EXISTS_ERROR':"Phone no and phone code already exists and cannot be updated",
    'PHONE_EMAIL_EXISTS_ERROR':"Phone no, phone code and email already exists and cannot be updated",
    'EMAIL_EXISTS_ERROR':"Email already exists and cannot be updated",
    'MISSING_PHONE_CODE_ERROR':"please enter PHONE CODE with phone no ",
    'NAME_ERROR':"Please enter your first name",
    'ANY_ONE_DETAIL_REQUIRED':"Please enter either phone no or email",
    'INVALID_GENDER':'Invalid Gender. Gender can only be male, female or others',
   
    'ITEM_NOT_FOUND' : "Item not found",
    'LANGUAGE_ALREADY_EXISTS' : "language_code or language_name already exists.",
    'DELETED_SUCCESSFULLY': "Successfully deleted",
    'NO_DATA_MESSAGE': "No data found",

       
    'INVALID_PH_NO' : "Invalid phone number format, please enter 10 digits.",
    'INVALID_EMAIL' : "Invalid email format.",
    'EXISTING_PH_NO' : "phone no already exists.",
    'EXISTING_EMAIL' : "Email Id already exists.",
    'EXPIRED_OTP' : "Your OTP has expired..",
    'INVALID_OTP' : "Invalid OTP code.",
    'INVALID_GENDER' : "Invalid Gender",
    'DETAILS_REQUIRED' : "Please provide email or phone number",
    'NO_USER_MESSAGE' : "User not found",
    'NO_PROFILE_MESSAGE' : "Profile not found",
    "NOT_AUTH":"Not authenticated.",
    'OTP_SUCCESS_MESSAGE': 'Otp sent successfully',
    'SERVER_ERROR_MSG': 'Internal Server Error',
    'SUCCESS_CREATED_MSG': 'Successfully Created',
    'SUCCESS_FETCHED_MSG': 'Successfully Fetched',
    'SUCCESS_VERIFIED_MSG': 'Successfully Verified',
    'SUCCESS_UPDATED_MSG': 'Successfully Updated',
    'USER_NOT_DELETED' : "user not found or invalid credentials",
    'USER_DELETED' : "Successfully deleted",
    'USER_LOGOUT' : "Successfully Logged out",
    'INVALID_GENDER':'Invalid Gender. Gender can only be male, female or others ',
    'PROFILE_EXISTS_MESSAGE':'Profile already exists',
    'NO_DOWNLOAD_MESSAGE':'Download not found',
    'DOWNLOAD_EXISTS':'Download already exists',

    'ROLE_EXISTS_MESSAGE':'Role already exists',
    'NO_PERMISSION_MESSAGE':'No Permissions found',
    'NO_ROLE_MESSAGE':'No Role found',
    'INVALID_ROLE':'Invalid user_role. Allowed values are: super_admin, admin, editor, author, subscriber'

}


