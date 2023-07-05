from api.db import *
from utils import *
from api.helper import *
from utils import *
from sqlalchemy.orm import Session


def fetch_app_languages(token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    result =  db.query(AppLanguage).all()
    if result:
        return result
    else:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NO_DATA_MESSAGE"]}

def add_app_language(request: AppLanguageBase, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    
    isUniqueAppLang = checkUniqueAppLang(request.language_code, request.language_name, db)
    if not isUniqueAppLang:
        return {"success": False, "code": common['ALREADY_EXISTING'], "message": common['LANGUAGE_ALREADY_EXISTS']}
    
    if isUniqueAppLang:
        app_lang = AppLanguage(
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
    

def app_language_update(id: str, request: AppLanguageBase, token: str, db: Session):
    user_token = db.query(Token).filter(Token.access_token == token).first()
    if not user_token:
        return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
    
    app_language = db.query(AppLanguage).filter(AppLanguage.id == id).first()
    if not app_language:
        return {"success": False, "code": common['NOT_FOUND'], "message": common['ITEM_NOT_FOUND']}
    
    app_language.language_code = request.language_code if request.language_code else app_language.language_code
    app_language.language_name = request.language_name if request.language_name else app_language.language_name
    app_language.language_text = request.language_text if request.language_text else app_language.language_text
    app_language.language_icon = request.language_icon if request.language_icon else app_language.language_icon
    app_language.status = request.status if request.status == False or request.status == True else app_language.status

    db.add(app_language)
    db.commit()
    
    updated_data = {
        "language_code": app_language.language_code,
        "language_name": app_language.language_name,
        "language_text": app_language.language_text,
        "language_icon": app_language.language_icon,
        "status": app_language.status
    }

    return updated_data
    


def app_language_delete(id: str, token: str, db: Session):
    app_lang = db.query(AppLanguage).get(id)
    if app_lang:
        user_token = db.query(Token).filter(Token.access_token == token).first()
        if not user_token:
            return {"success": False, "code": common['NOT_FOUND'], "message": common["NOT_AUTH"]}
        
        db.delete(app_lang)
        db.commit()
        return {"success": True, "code": common['SUCCESS'], "message": common['DELETED_SUCCESSFULLY']}

    return False