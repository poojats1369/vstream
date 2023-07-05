import mimetypes
import uuid
from api.db import *
from sqlalchemy.orm import Session

def add_file_to_system(file_data: FileSystemSchema, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "message": "Authentication failed."}

    object_id = file_data.object_id
    existing_file = db.query(FileSystem).filter(FileSystem.object_id == object_id).first()

    if existing_file:
        return {"success": False, "message": "File with the same object ID already exists."}

    filename = file_data.file_name
    mimetype, _ = mimetypes.guess_type(filename)
    
    file_system = FileSystem(
        file_id=uuid.uuid4().hex,
        object_id=file_data.object_id,
        object_type=file_data.object_type,
        file_name=file_data.file_name,
        path=file_data.path,
        created_at=datetime.utcnow(),
        updated_at=None,
        status=1,
        file_size=file_data.file_size,
        mime_type=mimetype,
        duration=file_data.duration if hasattr(file_data, 'duration') else None,
        thumbnail_path=file_data.thumbnail_path if hasattr(file_data, 'thumbnail_path') else None,
        description=file_data.description if hasattr(file_data, 'description') else None,
        is_public=file_data.is_public
    )

    db.add(file_system)
    db.commit()
    db.refresh(file_system)

    return {"success": True}



def get_file_details(fileId : str, token: str, db:Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()

    if not user_token:
        return {"success": False, "message": "Authentication failed."}
    
    file_system = db.query(FileSystem).filter(FileSystem.file_id == fileId).first()

    if not file_system:
        return {"success": False, "code": common['NOT_FOUND'], "message": "File not found"}

    return {"success": True, "file_details": file_system}


def update_file(request: FileSystemSchema, id: str, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    file = db.query(FileSystem).filter(id == FileSystem.file_id).first()
    if not file:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['ITEM_NOT_FOUND']}
    
    file.object_id = request.object_id if request.object_id else file.object_id
    file.object_type = request.object_type if request.object_type else file.object_type
    file.file_name = request.file_name if request.file_name else file.file_name
    file.path = request.path if request.path else file.path
    file.file_size = request.file_size if request.file_size else file.file_size
    file.mime_type = mimetypes.guess_type(file.file_name)
    file.duration = request.duration if request.duration else file.duration
    file.thumbnail_path = request.thumbnail_path if request.thumbnail_path else file.thumbnail_path
    file.description = request.description if request.description else file.description
    file.is_public = request.is_public if request.is_public == False or request.is_public == True else file.is_public

    db.add(file)
    db.commit()
    
    updated_data = {
        "object_id": file.object_id,
        "object_type": file.object_type,
        "file_name": file.file_name,
        "path": file.path,
        "file_size": file.file_size,
        "mime_type": file.mime_type,
        "duration": file.duration,
        "thumbnail_path": file.thumbnail_path,
        "description": file.description,
        "is_public": file.is_public,
    }

    return updated_data
    


def remove_file(id: str, token: str, db: Session):
    file = db.query(FileSystem).filter(id == FileSystem.file_id).first()
    if file:
        user_token = db.query(Token).filter(Token.access_token == token).first()
        if not user_token:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
        
        db.delete(file)
        db.commit()
        return {"success": True, "code": common['SUCCESS'], "message": common['DELETED_SUCCESSFULLY']}

    return False