from pydantic import BaseModel, constr, EmailStr, validator,BaseSettings,Field
from fastapi import HTTPException,FastAPI
from typing import List,Optional, Union
import enum
# from constants import *

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_no: Optional[str]
    phone_code: Optional[str]
    social_id: Optional[str]
    social_type: Optional[str]
    gender: Optional[str]
    profile_image: Optional[str]
    bio: Optional[str]
    latitude:Optional[str]
    longitude:Optional[str]
    date_of_birth: Optional[str]
    app_language: str = "English"

class DeviceBase(BaseModel):
    device_id: Optional[str]
    device_name: Optional[str]
    device_type: Optional[str]
    os: Optional[str]
    os_version: Optional[str]
    device_token: Optional[str]
    app_version: Optional[str]

class LoginBase(BaseModel):
    phone_no : Optional[str] = None
    phone_code : Optional[str] = None
    email : Optional[str] = None

class OtpBase(BaseModel):
    user_otp : str
    phone_no : Optional[str] = None
    phone_code : Optional[str] = None
    email : Optional[str] = None

class UpdateUserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone_no: Optional[str]
    phone_code: Optional[str]
    gender: Optional[str]
    profile_image: Optional[str]
    bio: Optional[str]
    latitude:Optional[str]
    longitude:Optional[str]
    date_of_birth: Optional[str]

class UpdateDeviceBase(BaseModel):
    device_token: Optional[str]
    app_version: Optional[str]

class UserProfileSchemaForGet(BaseModel):
    profile_id: str
    profile_name: Optional[str]
    profile_image: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    genre: Optional[List[str]]
    content_language: Optional[List[str]]
    pin: Optional[str]
    is_child: Optional[bool]
    status: Optional[bool]

#Mayank

class AppLanguageBase(BaseModel):
    language_code: Optional[str]
    language_name: Optional[str]
    language_text: Optional[str]
    language_icon: Optional[str]
    status: Optional[bool]

class ContentLanguageBase(BaseModel):
    language_code: Optional[str]
    language_name: Optional[str]
    language_text: Optional[str]
    language_icon: Optional[str]
    status: Optional[bool]

#Dheeraj and Anirudh

class UserProfileSchema(BaseModel):
    profile_name: Optional[str]
    profile_image: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    genre: Optional[List[str]]
    content_language: Optional[List[str]]
    app_language: Optional[str]
    pin: Optional[str]
    is_child: Optional[bool]
    status: Optional[bool]
    
class UserProfileIDSchema(BaseModel):
    profile_id: str
    profile_name: Optional[str]
    profile_image: Optional[str]
    date_of_birth: Optional[str]
    gender: Optional[str]
    genre: Optional[List[str]]
    content_language: Optional[List[str]]
    pin: Optional[str]
    is_child: Optional[bool]
    status: Optional[bool]

class ProfileDeleteSchema(BaseModel):
    profile_id: str

class PinUpdateSchema(BaseModel):
    profile_id: str
    pin: str

class WatchListSchema(BaseModel):
    profile_id: str
    content_id: str
    
class UpdateWatchListSchema(BaseModel):
    watchlist_id: str
    new_progress: str
