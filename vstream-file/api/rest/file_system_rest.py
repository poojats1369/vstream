from utils import *
from api.domain import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Header


file_system_router = APIRouter(prefix="/v1")

@file_system_router.post('/filesystem')
def create_file(file_data: FileSystemSchema, token: str = Header(), db: Session = Depends(get_db)):
# def create_file(file_data: FileSystemSchema, db: Session = Depends(get_db)):
    result = add_file_to_system(file_data, token, db)

    if result['success']:
        return {
            "response": {
                "code": 201,
                "status": "success",
                "alert": [{
                    "message": "File created successfully.",
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

@file_system_router.get('/filesystem')
def get_file(fileId: str,token: str = Header() ,db: Session = Depends(get_db)):  #,token: str = Header()
    result=get_file_details(fileId, token, db)
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
                "file_details":result['file_details']
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
    

@file_system_router.put("/filesystem")
def file_update(id: str, request: FileSystemSchema, token: str = Header(), db: Session = Depends(get_db)):
    result = update_file(id, request, token, db)
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
                "is_data": is_data,
                "data": result
            }
        }

@file_system_router.delete('/filesystem')
def delete_file(id: str, token: str = Header(), db: Session = Depends(get_db)):
    result = remove_file(id,token, db)
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