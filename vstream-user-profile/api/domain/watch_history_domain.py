import uuid
from api.db import *
from utils import *
from api.helper import *
from sqlalchemy.orm import Session
from sqlalchemy import desc

def get_watch_history_items(profile_id: str,token: str,db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['UNAUTHORIZED'], "message": common['NOT_AUTH']}    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()
    if not user:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}    
    user_profile = db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()    
    if not user_profile:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}
    try:
        watch_history_items = db.query(WatchHistoryItem).filter(WatchHistoryItem.user_profile_id == profile_id).order_by(desc(WatchHistoryItem.updated_at)).all()
        if watch_history_items:
            results = []
            for item in watch_history_items:
                watch_history_item = {
                    'id': item.id,
                    'watch_history_id': item.watch_history_id,
                    'content_id': item.content_id,
                    'watch_duration':item.watch_duration           
                }
                results.append(watch_history_item)
            return {"success": True, "watchhistory": results,"code":common['SUCCESS'],"message":common["SUCCESS_FETCHED_MSG"]}
        else:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["NO_CONTENT_MSG"]}
    except:
         return {"success": False, "code": common['SERVER_ERROR'], "message": common["SERVER_ERROR_MSG"]}
    

def add_to_watch_history_func(content_and_profile: WatchHistorySchema, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['UNAUTHORIZED'], "message": common['NOT_AUTH']}    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()
    if not user:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}    
    user_profile = db.query(UserProfile).filter(UserProfile.profile_id == content_and_profile.profile_id, UserProfile.user_id == content_and_profile.user_id).first()
    if not user_profile:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NO_USER_MESSAGE"]}
    try:    
        content_id = str(content_and_profile.content_id)  # Convert content_id to string
        existing_watchhistory_item = db.query(WatchHistoryItem).filter(
            WatchHistoryItem.user_id == user.user_id,
            WatchHistoryItem.user_profile_id == user_profile.profile_id,
            WatchHistoryItem.content_id == content_id
        ).first()
        if existing_watchhistory_item:
            return {"success": False, "code": common['ALREADY_EXISTING'], "message": common["ALREADY_EXISTING_MSG"]}
        content = db.query(Content).filter(Content.content_id == content_id).first()    
        if not content:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["NO_CONTENT_MSG"]}
        watch_history_item = WatchHistoryItem(
            watch_history_id=uuid.uuid4().hex,
            user_id=user.user_id,
            user_profile_id=user_profile.profile_id,
            content_id=content_id,
            watch_duration="00:00",
            created_at=datetime.utcnow() + timedelta(hours=5, minutes=30),
            updated_at=datetime.utcnow() + timedelta(hours=5, minutes=30)
        )
        db.add(watch_history_item)
        db.commit()
        db.refresh(watch_history_item)
        return {"success": True, "code": common['SUCCESS_CREATED'], "message": common["SUCCESS_CREATED_MSG"]}
    except:
        return {"success": False, "code": common['SERVER_ERROR'], "message": common["SERVER_ERROR_MSG"]}
    

def delete_watch_history_fun(token: str, id: int, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()    
    if not user_token:
        return {"success": False, "code":common['UNAUTHORIZED'], "message": common['NOT_AUTH']}
    try:
        watch_history_item = db.query(WatchHistoryItem).filter(WatchHistoryItem.id == id).first()    
        if watch_history_item:
            db.delete(watch_history_item)
            db.commit()
            return {"success": True, "code":common['SUCCESS'], "message": common["USER_DELETED"]}        
        return {"success": False, "code":common['NOT_FOUND'], "message": common["FAILURE_MSG"]}
    except:
         return {"success": False, "code": common['SERVER_ERROR'], "message": common["SERVER_ERROR_MSG"]}


def update_watch_duration_fun(updatewatchhistory:UpdateWatchHistorySchema,token: str,  db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['UNAUTHORIZED'], "message": common['NOT_AUTH']}
    try:
        watch_history_item = db.query(WatchHistoryItem).filter(WatchHistoryItem.id == updatewatchhistory.id).first()
        if watch_history_item:
            watch_history_item.watch_duration = updatewatchhistory.new_duration
            watch_history_item.updated_at = datetime.utcnow() + timedelta(hours=5, minutes=30)
            db.commit()
            return {"success": True, "code": common['SUCCESS'], "message": common["SUCCESS_UPDATED_MSG"],"data":watch_history_item}
        else:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["FAILURE_MSG"]}
    except:
          return {"success": False, "code": common['SERVER_ERROR'], "message": common["SERVER_ERROR_MSG"]}