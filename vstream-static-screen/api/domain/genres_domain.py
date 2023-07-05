from utils import *
from api.db import *
from api.db.schemas import *
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from api.helper import *
from utils import *

def genre_add(genre_data: GenreBase, token:str,db: Session = Depends(get_db)):

    token_entry = db.query(Token).filter(Token.access_token == token).first()
    if token_entry:
        try:
            genre_check = db.query(Genre).filter(Genre.genre_name == genre_data.genre_name).first()
            if genre_check:
                return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['ALREADY_EXISTING_MSG']}
            
            genre_code = genre_code_generate(genre_data.genre_name)          
            genre = Genre(
                genre_code = genre_code.lower(),
                genre_name = genre_data.genre_name,
                genre_description = genre_data.genre_description,
                genre_type=genre_data.genre_type
            )
            db.add(genre)
            db.commit()
            return {"success": True, "code": common['SUCCESS'], "message": common['SUCCESS_CREATED_MSG']}
        except:
             return {"success": False, "code": common['SERVER_ERROR'], "message": common['SERVER_ERROR_MSG']}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['APP_TOKEN_MISSING']}



def genres_get(token:str,db:Session):
    token_entry = db.query(Token).filter(Token.access_token == token).first()
    if token_entry:
        try:
            all_data=db.query(Genre).order_by(desc(Genre.created_at)).all()
            if all_data:
                return{"success": True, "data":all_data }
            else:
                return {"success": False, "code": common['NOT_FOUND'], "message": common['FAILURE_MSG']}
        except:
            return {"success": False, "code": common['SERVER_ERROR'], "message": common['SERVER_ERROR_MSG']}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['APP_TOKEN_MISSING']}
    
def genre_update(genre_id: int, genre_data: GenreUpdateBase,token:str, db: Session):
    token_entry = db.query(Token).filter(Token.access_token == token).first()
   
    if token_entry:
        try:           
            genre = db.query(Genre).filter(Genre.id == genre_id).first()
            if genre:
                if genre_data.genre_name:
                    genre_code = genre_code_generate(genre_data.genre_name)  
                genre.genre_code=genre_code if genre_data.genre_name else genre.genre_code
                genre.genre_name = genre_data.genre_name if genre_data.genre_name else  genre.genre_name
                genre.genre_description = genre_data.genre_description if genre_data.genre_description else genre.genre_description
                genre.genre_type = genre_data.genre_type if genre_data.genre_type else  genre.genre_type
                db.commit()           
                return {"success":True,"Genre":genre}
            else:
                return {"success": False, "code": common['NOT_FOUND'], "message": common['FAILURE_MSG']}
        except:
            return {"success": False, "code": common['SERVER_ERROR'], "message": common['SERVER_ERROR_MSG']}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['APP_TOKEN_MISSING']}

def genre_delete(genre_id: int,token:str, db:Session):
    token_entry = db.query(Token).filter(Token.access_token == token).first()
    if token_entry:
        try:
            genre = db.query(Genre).filter(Genre.id == genre_id).first()
            if genre:
                db.delete(genre)
                db.commit()
                return {"success": True, "code": common['SUCCESS'], "message": common['USER_DELETED']}
            else:
                return {"success": False, "code": common['NOT_FOUND'], "message": common['FAILURE_MSG']}
        except:
            return {"success": False, "code": common['SERVER_ERROR'], "message": common['SERVER_ERROR_MSG']}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['APP_TOKEN_MISSING']}