from fastapi import Depends, APIRouter,Header
from sqlalchemy.orm import Session
from api.db.schemas import *
from api.db import *
from api.domain import *
from utils import *
from api.helper import *
from utils import *
from api.domain.genres_domain import *

genre_router = APIRouter(prefix="/v1")

@genre_router.post("/genres")
def add_genre(genre_data: GenreBase, token:str=Header(),db: Session = Depends(get_db)):
    result = genre_add(genre_data,token,db)
    if result['success']:
        return {
            "response": {
                "code": result["code"],
                "status": "success",
                "is_data": 0,
                "alert": [{
                    "message": result["message"],
                    "type": "created",
                }]                
            }
        }
    else:
        return {
            "response": {
                "code": result["code"],
                "status": "failure",
                "is_data": 0,
                "alert": [{
                    "message": result["message"],
                    "type": "failure",
                }],
                
            }
        }


@genre_router.get("/genres")
def get_genres(token:str=Header(),db: Session = Depends(get_db)):
    result=genres_get(token,db)
    is_data = 1 if result["success"] else 0
    if result["success"]:
        genre_list = []
        for genre in result["data"]:
            genre_values = {
                "genre_code":genre.genre_code,
                "genre_name": genre.genre_name,
                "genre_description": genre.genre_description,
                "status": genre.status,
                "genre_type":genre.genre_type,
                "genre_id":genre.id
            }
            genre_list.append(genre_values)

        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "is_data":is_data,
                "alert": [{
                    "message": common['SUCCESS_FETCHED_MSG'],
                    "type": "Fetch"                    
                }],                
                "genre": genre_list
              
                
            }
        }
    else:
        return {
            "response": {
                "code": common['FAILURE'],
                "status": "failure",
                "is_data":is_data,
                "alert": [{
                    "message":  common['NO_CONTENT_MSG'],
                    "type": "failure"
                }]
            }
        }


@genre_router.put("/genres")
def update_genre(genre_id: int, genre_data: GenreUpdateBase, token: str = Header(), db: Session = Depends(get_db)):
    result = genre_update(genre_id, genre_data, token, db)
    is_data = 1 if result["success"] else 0
    if result["success"]:
        genre_data = {
            "genre_name": result["Genre"].genre_name,
            "genre_description": result["Genre"].genre_description,
            "genre_type": result["Genre"].genre_type,
            "genre_code": result["Genre"].genre_code,
            "genre_id":  result["Genre"].id,
        }
        return {
            "response": {
                "code": common['SUCCESS'],
                "status": "success",
                "is_data": is_data,
                "alert": [{
                    "message": common['SUCCESS_UPDATED_MSG'],
                    "type": "Update",
                }],                
                "data": genre_data
            }
        }
    else:
        return {
            "response": {
                "code": common['NOT_FOUND'],
                "status": "Failure",
                "is_data": is_data,
                "alert": [{
                    "message": common['FAILURE_MSG'],
                    "type": "Failure"
                }]
               
            }
        }
    
@genre_router.delete("/genres")
def delete_genre(genre_id: int,token:str=Header(),db: Session = Depends(get_db)):

    result = genre_delete(genre_id,token, db)
    if result["success"]:
        return {
            "response": {
                "code": result["code"],
                "status": "success",
                "is_data": 0,
                "alert": [{
                    "message": result["message"],
                    "type": "deleted"
                }],
            }
        }
    else:
        return {
            "response": {
                "code":result["code"],
                "status": "failure",
                "is_data": 0,
                "alert": [{
                    "message": result["message"],
                    "type": "failure"
                }],
            }
        }
