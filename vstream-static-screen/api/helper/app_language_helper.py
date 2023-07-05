from api.db import *
from sqlalchemy.orm import Session

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def checkUniqueAppLang(lang_code: str, lang_name: str, db: Session):
    langCode = db.query(AppLanguage).filter(lang_code == AppLanguage.language_code).first()
    langName = db.query(AppLanguage).filter(lang_name == AppLanguage.language_name).first()

    if langCode or langName:
        return False
    return True
