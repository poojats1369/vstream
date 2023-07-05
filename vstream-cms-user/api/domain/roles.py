import uuid
from api.db import *
from utils import *
from fastapi import Depends
from api.helper.helper import *
from sqlalchemy.orm import Session

def role_add(role_data: RoleSchema, db: Session = Depends(get_db)):
    user_role = db.query(UserRoles).filter_by(role_name=role_data.role_name).first()
    if user_role:
        return False
    role = UserRoles(
        id = uuid.uuid4().hex,
        role_name = role_data.role_name,
        permissions = role_data.permissions,
        status = role_data.status
    )
    db.add(role)
    db.commit()
    return True

def roles_get(db:Session):
    return db.query(UserRoles).all()

def role_update(role_id: str, role_data: RoleSchema, db: Session):
    role = db.query(UserRoles).filter_by(id=role_id).first()
    if role:
        role.permissions = role_data.permissions
        role.status = role_data.status
        db.commit()
        return role
    else:
        return None

def role_delete(role_id:str, db:Session):
    role = db.query(UserRoles).get(role_id)
    if role:
        db.delete(role)
        db.commit()
        return True
    else:
        False