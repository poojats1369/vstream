import uuid
from api.db import *
from utils import *
from api.helper import *
from fastapi import Depends
from sqlalchemy.orm import Session

def get_profiles_logged_in(token:str, db:Session):

    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    profiles = db.query(UserProfile).filter(UserProfile.user_id == user_token.user_id).all()
    user_profiles = []
    for profile in profiles:
        user_profiles.append(prepare_response_profile(profile))
    if not user_profiles:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}
    
    return {"success": True, "details": user_profiles}

def get_profile_by_id(token:str, profile_id: str, db:Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()
    profile = db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()

    if not user or not profile:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}
    
    return {"success": True, "details": prepare_response_profile(profile)}

def profile_delete(token: str, profile_id: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    
    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    profile = db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()

    if profile:
        db.delete(profile)
        db.commit()
        return {"success": True, "code":common['SUCCESS'], "message": common['USER_DELETED']}
    
    return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}

def register_profile(token: str, user_profile: UserProfileSchema, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    unique_profile = check_unique_profile(user_profile.profile_name, user_token, db)
    if not unique_profile:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['PROFILE_EXISTS_MESSAGE']}

    if user_profile.gender.lower() not in ['male','female','other']:
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}
    
    user_profile.gender = user_profile.gender.upper()

    new_profile = UserProfile(profile_id=uuid.uuid4().hex, user_id=user_token.user_id, **user_profile.dict())
    
    db.add(new_profile)
    db.commit()

    profiles = db.query(UserProfile).filter(UserProfile.user_id == user_token.user_id).all()
    user_profiles = []
    for profile in profiles:
        user_profiles.append(prepare_response_profile(profile))
  
    return {"success": True, "details": user_profiles}

def profiles_update(token: str, user_profile: UserProfileIDSchema, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    existing_profile = db.query(UserProfile).filter(UserProfile.profile_id == user_profile.profile_id).first()

    if not existing_profile:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}
    
    if user_profile.profile_name:
        unique_profile = check_unique_profile(user_profile.profile_name, user_token, db)
        if not unique_profile:
            return {"success": False, "code":common['NOT_FOUND'], "message": common['PROFILE_EXISTS_MESSAGE']}
    
    if user_profile.gender.lower() not in ['male','female','other']:
        return {"success": False, "code": common['FAILURE'], "message": common['INVALID_GENDER']}
    
    if not user_profile.profile_name:
        user_profile.profile_name = existing_profile.profile_name
       
    for key, value in user_profile.dict().items():
        setattr(existing_profile, key, value)

    db.commit()

    return {"success": True, "details": prepare_response_profile(existing_profile)}

def prepare_response_profile(profile: UserProfileIDSchema):
    return {
        "profile_id": profile.profile_id,
        "profile_name": profile.profile_name,
        "profile_image": profile.profile_image,
        "date_of_birth": profile.date_of_birth,
        "gender": profile.gender,
        "content_language": profile.content_language,
        "genre": profile.genre,
        "pin": profile._pin,
        "is_child": profile.is_child,
        "status": profile.status
    }

def check_unique_profile(profile_name: str, user_token: Token, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_token.user_id).first()
    profiles = db.query(UserProfile).filter(UserProfile.user_id == user.user_id).all()
    for profile in profiles:
        if profile.profile_name == profile_name:
            return False
    return True

