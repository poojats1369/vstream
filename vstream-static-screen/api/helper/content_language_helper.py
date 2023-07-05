from api.db import *
from sqlalchemy.orm import Session

def checkUniqueContentLang(lang_code: str, lang_name: str, db: Session):
    langCode = db.query(ContentLanguage).filter(lang_code == ContentLanguage.language_code).first()
    langName = db.query(ContentLanguage).filter(lang_name == ContentLanguage.language_name).first()

    if langCode or langName:
        return False
    return True
