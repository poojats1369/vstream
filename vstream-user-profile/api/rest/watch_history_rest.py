from api.db import *
from utils import *
from api.domain import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

watch_history_router = APIRouter(prefix="/v1")

@watch_history_router.get('/watch-history')
def get_watch_history(profileId: str,token: str = Header(),db: Session = Depends(get_db)):
    result=get_watch_history_items(profileId,token ,db)
    is_data = 1 if result['success'] else 0
    if result['success']:
        return {
            "response": {
                "code": result["code"],
                "status": "success",
                "alert": [{
                    "message": result["message"],
                    "type": "Fetch"
                }],
                "is_data":is_data,                
                "watchhistory":result['watchhistory']
            }
        }
    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data":is_data 
            }
        }

@watch_history_router.post('/watch-history')
def add_to_watch_history(content_and_profile: WatchHistorySchema, token: str=Header(), db: Session = Depends(get_db)):
    result = add_to_watch_history_func(content_and_profile,token,db)
    if result['success']:
        return {
            "response": {
                "code": result["code"],
                "status": "success",
                "alert": [{
                    "message": result["message"],
                    "type": "created",
                }],
                "is_data": 0
            }
        }
    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                "is_data": 0
            }
        }
    
@watch_history_router.delete("/watch-history")
def delete_watch_history( id: int,token: str=Header(), db: Session = Depends(get_db)):
    result = delete_watch_history_fun(token, id, db)
    if result['success']:
        return {
            "response": {
                "code":  result["code"],
                "status": "success",
                "alert": [{
                    "message": result["message"],
                    "type": "delete",
                }],
                "is_data": 0
            }
        }
    else:
        return {
            "response": {
                "code":result["code"],
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
                "is_data": 0
            }
        }

@watch_history_router.put("/watch-history")
def update_watch_duration(updatewatchhistory :UpdateWatchHistorySchema , token: str=Header(), db: Session = Depends(get_db)):
    result = update_watch_duration_fun(updatewatchhistory,token, db) 
    is_data = 1 if result["success"] else 0 
    if result["success"]:
        return {
            "response": {
                "code": result["code"],
                "status": "Success",
                "alert": [{
                    "message": result["message"],
                    "type": "Update"
                }],
                "is_data": is_data,
                "data":{
                    "id":result["data"].id,
                    "content_id":result["data"].content_id,
                    "watch_duration":result["data"].watch_duration
                }
            }
        }

    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "alert": [{
                    "message": result["message"],
                    "type": "Update"
                }],
                "is_data": is_data
            }
        }
