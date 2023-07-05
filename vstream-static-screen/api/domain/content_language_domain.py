from api.db import *
from utils import *
from api.helper import *
from utils import *
from sqlalchemy.orm import Session



def fetch_content_languages(token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    result =  db.query(ContentLanguage).all()
    if result:
        return result #{"success": True, "code": common['SUCCESS'], "message": common["SUCCESS_FETCHED_MSG"],"data":result}
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NO_DATA_MESSAGE"]}

def add_content_language(request: ContentLanguageBase, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    
    isUniqueContentLang = checkUniqueContentLang(request.language_code, request.language_name, db)
    if not isUniqueContentLang:
        return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['LANGUAGE_ALREADY_EXISTS']}
    
    if isUniqueContentLang:
        app_lang = ContentLanguage(
            language_code = request.language_code,
            language_name = request.language_name,
            language_text = request.language_text,
            language_icon = request.language_icon,
            status = request.status,
        )
        db.add(app_lang)
        db.commit()

        return {"success": True}
    else:
        return {"success": False}
    

def content_language_update(id: str, request: ContentLanguageBase, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    
    content_language = db.query(ContentLanguage).filter(ContentLanguage.id == id).first()
    if not content_language:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['ITEM_NOT_FOUND']}
    
    content_language.language_code = request.language_code if request.language_code else content_language.language_code
    content_language.language_name = request.language_name if request.language_name else content_language.language_name
    content_language.language_text = request.language_text if request.language_text else content_language.language_text
    content_language.language_icon = request.language_icon if request.language_icon else content_language.language_icon
    content_language.status = request.status if request.status == False or request.status == True else content_language.status

    db.add(content_language)
    db.commit()
    
    updated_data = {
        "language_code": content_language.language_code,
        "language_name": content_language.language_name,
        "language_text": content_language.language_text,
        "language_icon": content_language.language_icon,
        "status": content_language.status
    }

    return updated_data
    


def content_language_delete(id: str, token: str, db: Session):
    content_lang = db.query(ContentLanguage).get(id)
    if content_lang:
        user_token = db.query(Token).filter(Token.access_token == token).first()
        if not user_token:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
        
        db.delete(content_lang)
        db.commit()
        return {"success": True, "code": common['SUCCESS'], "message": common['DELETED_SUCCESSFULLY']}

    return False