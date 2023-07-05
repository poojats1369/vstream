
import uuid
from utils import *
from api.db import *
from fastapi import Depends
from sqlalchemy.orm import Session
from api.helper.helper import *

def permission_add(permission_data: PermissionSchema, db: Session = Depends(get_db)):
    user_permissions = db.query(UserPermissions).filter_by(permission_name=permission_data.permission_name).first()
    if user_permissions:
        return False
    else:
        user_permissions = UserPermissions(
            id=uuid.uuid4().hex,
            permission_name = permission_data.permission_name,
            permission_type = permission_data.permission_type,
            collection = permission_data.collection,
            status = permission_data.status
        )
        db.add(user_permissions)
        db.commit()
    return user_permissions

def permission_get(db):
    return db.query(UserPermissions).all()

def permissions_update(perm_id, perm_data, db):
    user_perm = db.query(UserPermissions).filter_by(id=perm_id).first()
    if user_perm:
        user_perm.permission_name = perm_data.permission_name
        user_perm.permission_type = perm_data.permission_type
        user_perm.collection = perm_data.collection

        db.add(user_perm)
        db.commit()
        return user_perm
    else:
        False

def permission_delete(perm_id:str, db:Session):
    perm = db.query(UserPermissions).get(perm_id)
    if perm:
        db.delete(perm)
        db.commit()
        return True
    else:
        False