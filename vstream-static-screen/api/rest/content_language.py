from api.db import *
from utils import *
from api.domain import *
from api.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header

content_language_router = APIRouter(prefix="/v1")

@content_language_router.get("/content-language")
def get_content_languages(token: str = Header(), db: Session = Depends(get_db)):
    result = fetch_content_languages(token, db)
    is_data = 1 if result else 0 
    if result and ("code" in result and "message" in result):
    # if result["success"]:
        return {
            "response": {
                "code": result["code"],
                "status": "Failure",
                "alert": [{
                    "message": result["message"],
                    "type": "Failure"
                }],
                "is_data": 0
            }
        }

    else:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"
                }],
                "is_data": is_data,
                "data": result
            }
        }


@content_language_router.post("/content-language")
def create_content_language(request: AppLanguageBase, token: str = Header(), db: Session = Depends(get_db)):
    result = add_content_language(request, token, db)
    is_data = 1 if result else 0 
    if "code" in result and "message" in result:
        return {
            "response": {
                "code": result["code"],
                "status": "Failure",
                "alert": [{
                    "message": result["message"],
                    "type": "Failure"
                }],
                "is_data": 0
            }
        }

    else:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "Success",
                "alert": [{
                    "message": common['SUCCESS_CREATED_MSG'],
                    "type": "Create"
                }],
                "is_data": 0,
            }
        }


@content_language_router.put("/content-language")
def update_content_language(id: str, request: AppLanguageBase, token: str = Header(), db: Session = Depends(get_db)):
    result = content_language_update(id, request, token, db)
    is_data = 1 if result else 0 
    if "code" in result and "message" in result:
        return {
            "response": {
                "code": result["code"],
                "status": "Failure",
                "alert": [{
                    "message": result["message"],
                    "type": "Failure"
                }],
                "is_data": is_data
            }
        }

    else:
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "alert": [{
                    "message": common['SUCCESS_UPDATED_MSG'],
                    "type": "Update"
                }],
                "is_data": 0,
                "data": result
            }
        }
    

@content_language_router.delete("/content-language")
def delete_content_language(id: str, token: str = Header(), db: Session = Depends(get_db)):
    result = content_language_delete(id,token, db)
    if result:
        if result['success']:
            return {
                "response": {
                    "code": result['code'],
                    "status": "success",
                    "alert": [{
                        "message": result['message'],
                        "type": "delete",
                    }]
                }
            }
        else: return {
            "response": {
                "code": result['code'],
                "status": "failure",
                "alert": [{
                    "message": result['message'],
                    "type": "failure"
                }],
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "failure",
                "alert": [{
                    "message": common['ITEM_NOT_FOUND'],
                    "type": "failure"
                }],
            }
        }
