from api.db import *
from utils import *
from api.domain import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

watchlist_router = APIRouter(prefix="/v1")

@watchlist_router.get('/watchlist')
def get_watchlist_items(profileId: str ,token: str = Header(),db: Session = Depends(get_db)):  #,token: str = Header()
    result=get_watchlist_items_using_profileId(profileId,token ,db)
    is_data = 1 if result['success'] else 0

    if result['success']:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"
                }],
                "is_data":is_data,                
                "watchlist":result['watchlist']
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }

@watchlist_router.post('/watchlist')
def add_to_watchlist(content_and_profile: WatchListSchema, token: str = Header(), db: Session = Depends(get_db)):
    result=add_to_watchlists(content_and_profile,token,db)

    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": 201,
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "created",
                }],
                "is_data": 0
            }
        }
    else:
        return {
            "response": {
                "code": 500,
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                "is_data": 0
            }
        }
    
@watchlist_router.delete("/watchlist")
def delete_watchlist( watchlist_id: str,token: str = Header(), db: Session = Depends(get_db)):
    result = watchlist_item_delete(token, watchlist_id, db)
    if result['success']:
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": "DELETED_FROM_WATCHLIST",
                    "type": "delete",
                }],
                "is_data": 0
            }
        }
    else:
        return {
            "response": {
                "code": 404,
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data": 0
            }
        }

@watchlist_router.put("/watchlist")
def update_watch_progress(updatewatchlist :UpdateWatchListSchema , token: str = Header(), db: Session = Depends(get_db)):

    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['NOT_AUTH']}

    watchlist = db.query(WatchlistItem).filter(WatchlistItem.watchlist_id == updatewatchlist.watchlist_id).first()

    if watchlist:
        watchlist.watch_progress = updatewatchlist.new_progress
        watchlist.updated_at = datetime.now()

        db.commit()
        return {
            "response": {
                "code": 200,
                "status": "success",
                "alert": [{
                    "message": "WATCH_PROGRESS_UPDATED",
                    "type": "update",
                }],
                "is_data": 0
            }
        }
    else:
        return {
            "response": {
                "code": 404,
                "status": "failure",
                "alert": [{
                    "message": "INVALID_WATCHLIST_ID",
                    "type": "failure"
                }],
                "is_data": 0
            }
        }

