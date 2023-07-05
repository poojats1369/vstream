import uuid
from api.db import *
from utils import *
from sqlalchemy.orm import Session

def get_watchlist_items_using_profileId(profile_id: str,token: str,db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()

    if not user:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}
    
    user_profile = db.query(UserProfile).filter(UserProfile.profile_id == profile_id).first()
    
    if not user_profile:
        return {"success": False, "code": common['NOT_FOUND'], "message": "PROFILE_NOT_FOUND_BY _THIS_ID"}
    
    
    watchlist_items = db.query(WatchlistItem).filter(WatchlistItem.user_profile_id == profile_id).all()
    results = []

    for item in watchlist_items:
        watchlist_item = {
            'id': item.id,
            'watchlis_id': item.watchlist_id,
            'content_id': item.content_id,
            'watchprogress':item.watch_progress
           
        }
        results.append(watchlist_item)

    return {"success": True, "watchlist": results}


def add_to_watchlists(content_and_profile: WatchListSchema, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    user = db.query(User).filter(User.user_id == user_token.user_id).first()

    if not user:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NO_USER_MESSAGE']}
    
    user_profile = db.query(UserProfile).filter(UserProfile.profile_id == content_and_profile.profile_id).first()
    
    if not user_profile:
        return {"success": False, "code": common['NOT_FOUND'], "message": "PROFILE_NOT_FOUND_BY _THIS_ID"}
    
    content_id = str(content_and_profile.content_id)  # Convert content_id to string
    existing_watchlist_item = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == user.user_id,
        WatchlistItem.user_profile_id == user_profile.profile_id,
        WatchlistItem.content_id == content_id
    ).first()
    
    if existing_watchlist_item:
        return {"success": False, "code": 'ALREADY_EXISTS', "message": "WATCHLIST_ITEM_ALREADY_EXISTS"}

    content = db.query(Content).filter(Content.content_id == content_id).first()
    
    if not content:
        return {"success": False, "code": common['NOT_FOUND'], "message": "CONTENT_NOT_FOUND_BY_THIS_ID"}

    watchlist_item = WatchlistItem(
        watchlist_id=uuid.uuid4().hex,
        user_id=user.user_id,
        user_profile_id=user_profile.profile_id,
        content_id=content_id,
        watch_progress="00:00",
        created_at=datetime.utcnow() + timedelta(hours=5, minutes=30)
    )
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)

    return {"success": True}


def watchlist_item_delete(token: str, watchlist_id: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    
    if not user_token:
        return {"success": False, "code":common['NOT_FOUND'], "message": common['NOT_AUTH']}
    
    watchlist = db.query(WatchlistItem).filter(WatchlistItem.watchlist_id == watchlist_id).first()
    
    

    if watchlist:
        db.delete(watchlist)
        db.commit()
        return {"success": True, "code":common['SUCCESS'], "message": "CONTENT_DELETED_FROM_WATCHLIST"}
    
    return {"success": False, "code":common['NOT_FOUND'], "message": "INVALID_WATCHLIST_ID"}




def update_watch_progress(token: str, watchlist_id: str, new_progress: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}

    watchlist = db.query(WatchlistItem).filter(WatchlistItem.watchlist_id == watchlist_id).first()

    if watchlist:
        watchlist.watch_progress = new_progress
        watchlist.updated_at = datetime.now()

        db.commit()
        return {"success": True, "code": common['SUCCESS'], "message": "WATCH_PROGRESS_UPDATED"}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": "INVALID_WATCHLIST_ID"}
