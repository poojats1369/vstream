import uuid
from fastapi import Depends
from api.db import *
from utils import *
from sqlalchemy.orm import Session

from utils import *

def get_profile_downloads(token:str, profile_id: str, db:Session):

    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    profile = db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()
    if not profile:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}
    
    downloads = db.query(DownloadList).filter(DownloadList.profile_id == profile_id).all()
    if not downloads:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_DOWNLOAD_MESSAGE']}
    
    for download in downloads:
        if datetime.now() >= download.expiry_datetime:
            download.is_expired=True
            db.add(download)
            db.commit()

    profile_downloads = []
    for download in downloads:
        content = db.query(Content).filter(Content.content_id == download.content_id).first()
        if download.is_expired==True:
            continue       
        profile_downloads.append(prepare_response_download(download, content))
    return {"success": True, "details": profile_downloads}

def get_download_by_id(token:str, download_id: str, db:Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    download = db.query(DownloadList).filter(DownloadList.download_id == download_id).first()
    if not download:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_DOWNLOAD_MESSAGE']}
    
    content = db.query(Content).filter(Content.content_id == download.content_id).first()
   
    if datetime.now() >= download.expiry_datetime:
        download.is_expired=True
        db.add(download)
        db.flush()
        return {"success": False, "code":common['NOT_FOUND'], "message": common['EXPIRED_DOWNLOAD']}

    return {"success": True, "details": prepare_response_download(download, content)}

def download_delete(token: str, download_id: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    
    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    download = db.query(DownloadList).filter(DownloadList.download_id == download_id).first()
    if not download:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_DOWNLOAD_MESSAGE']}
    content = db.query(Content).filter(Content.content_id == download.content_id).first()

    db.delete(download)
    db.delete(content)
    db.commit()
    return {"success": True, "code":common['SUCCESS'], "message": common['USER_DELETED']}
    

def post_download(token: str, user_download: DownloadSchema, user_content: ContentDetails, db: Session = Depends(get_db)):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    user = db.query(User).filter(User.user_id == user_download.user_id).first()
    if not user:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}
    
    profile = db.query(UserProfile).filter(UserProfile.profile_id == user_download.profile_id).first()
    if not profile:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_PROFILE_MESSAGE']}
    
    device = db.query(Device).filter(Device.device_id == user_download.device_id).first()
    if not device:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_DEVICE_MESSAGE']}
    
    current_time = datetime
    expiry_time = current_time + timedelta(hours=48)
    
    download_unique = check_unique_download(user_download, user_content, db)
    if not download_unique:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['DOWNLOAD_EXISTS']}
    
    new_content_id=uuid.uuid4().hex

    new_download = DownloadList(download_id=uuid.uuid4().hex,  expiry_datetime=expiry_time, **user_download.dict())
    
    db.add(new_download)
    db.flush()

    new_content = Content(content_id = new_content_id, **user_content.dict())

    db.add(new_content)
    new_download.content_id = new_content.content_id
    db.commit()

    downloads = db.query(DownloadList).filter(DownloadList.profile_id == user_download.profile_id).all()
    profile_downloads = []
    for download in downloads:
        content = db.query(Content).filter(Content.content_id == download.content_id).first()
        if not content:
            return {"success": False, "code":common['NOT_FOUND'], "message": common['NO_CONTENT_FOUND']}
        if download.is_expired==True:
            return {"success": False, "code":common['NOT_FOUND'], "message": common['EXPIRED_DOWNLOAD']}
       
        profile_downloads.append(prepare_response_download(download, content))
    
    return {"success": True, "details": profile_downloads}

def prepare_response_download(download: DownloadIDSchema, content: ContentIDDetails):
    return {
        "download_id": download.download_id,
        "location": download.location,
        "download_url": download.download_url,
        "download_size": download.download_size,
        "download_quality": download.download_quality,
        "download_format": download.download_format,
        "subtitle_language": download.subtitle_language,
        "audio_language": download.audio_language,
        "download_duration": download.download_duration,
        "content": prepare_response_content(content)
    }

def prepare_response_content(content: ContentIDDetails):
    return {
        "content_id": content.content_id,
        "title": content.title,
        "description": content.description,
        "thumbnail_url": content.thumbnail_url,
        "duration": content.duration,
        "genre": content.genre,
        "release_date": content.release_date,
        "director": content.director,
        "actors": content.actors
    }

def check_unique_download(user_download: DownloadSchema, user_content: ContentIDDetails, db: Session = Depends(get_db)):
    downloads = db.query(DownloadList).filter(DownloadList.profile_id == user_download.profile_id).all()
    content = db.query(Content).filter(Content.title == user_content.title).first()

    if content:
        return False
    
    for download in downloads:
        if download.download_url == user_download.download_url:
            return False
    
    return True

