# from fastapi import Depends, APIRouter, Header
# from sqlalchemy.orm import Session 
# from api.db.schemas import *
# from utils import *
# from api.domain import *


# download_router = APIRouter(prefix="/v1")

# @download_router.post("/downloads")
# def create_download(download: DownloadSchema,  content: ContentDetails, token: str=Header(), db: Session = Depends(get_db)):
#     result = post_download(token, download, content, db)
#     is_data = 1 if result['success'] else 0
#     if result['success']:
#         return {
#             "response": {
#                 "code": 201,
#                 "status": "success",
#                 "alert": [{
#                     "message": common['SUCCESS_CREATED_MSG'],
#                     "type": "created",
#                 }],
#                 "is_data": is_data,
#                 "data":result['details']
#             }
#         }
#     else:
#         return {
#             "response": {
#                 "code": 500,
#                 "status": "failure",
#                 "alert": [{
#                     "message": result["message"],
#                     "type": "failure",
#                 }],
#                 "is_data": is_data
#             }
#         }

# @download_router.get('/downloads')
# def get_downloads( profile_id:str, token: str=Header(), db: Session = Depends(get_db)):
#     result = get_profile_downloads(token, profile_id, db)
#     is_data = 1 if result['success'] else 0
#     if result['success']:
#         return {
#             "response": {
#                 "code": 200,
#                 "status": "success",
#                 "alert": [{
#                     "message": common['SUCCESS_FETCHED_MSG'],
#                     "type": "Fetch"
#                 }],
#                 "is_data":is_data,                
#                 "data":result['details']
#             }
#         }
#     else:
#         return {
#             "response": {
#                 "code": 404,
#                 "status": "failure",
#                 "alert": [{
#                     "message": result['message'],
#                     "type": "failure"
#                 }],
#                 "is_data":is_data 
#             }
#         }
    
# @download_router.get("/download")
# def get_download( download_id: str,token: str=Header(), db: Session = Depends(get_db)):
#     result = get_download_by_id(token, download_id, db)
#     is_data = 1 if result['success'] else 0
#     if result['success']:
#         return {
#             "response": {
#                 "code": 200,
#                 "status": "success",
#                 "alert": [{
#                     "message": common['SUCCESS_FETCHED_MSG'],
#                     "type": "Fetch"
#                 }],
#                 "is_data":is_data,                
#                 "data":result['details']
#             }
#         }
#     else:
#         return {
#             "response": {
#                 "code": 404,
#                 "status": "failure",
#                 "alert": [{
#                     "message": result['message'],
#                     "type": "failure"
#                 }],
#                 "is_data":is_data 
#             }
#         }
    
# @download_router.delete("/downloads")
# def delete_download( download_id: str,token: str=Header(), db: Session = Depends(get_db)):
#     result = download_delete(token, download_id, db)
#     if result['success']:
#         return {
#             "response": {
#                 "code": 200,
#                 "status": "success",
#                 "alert": [{
#                     "message": common['USER_DELETED'],
#                     "type": "delete",
#                 }]
#             }
#         }
#     else:
#         return {
#             "response": {
#                 "code": 404,
#                 "status": "failure",
#                 "alert": [{
#                     "message": result['message'],
#                     "type": "failure"
#                 }],
#             }
#         }
 