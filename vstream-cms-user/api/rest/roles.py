from api.db import *
from api.domain import *
from api.helper.helper import *
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from utils import *

roles_router = APIRouter()

@roles_router.post("/roles")
def add_role(role_data: RoleSchema, db: Session = Depends(get_db)):
    result = role_add(role_data,db)
    if result:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_CREATED_MSG"],# "New role added successfully",
                    "type": "created",
                }]
            }
        }
    else:
        return {
            "response": {
                "code": common["SERVER_ERROR"],
                "status": "failure",
                "alert": [{
                    "message":common["ROLE_EXISTS_MESSAGE"],# "Role already exists | internal server error",
                    "type": "failure",
                }],
            }
        }

@roles_router.get("/roles")
def get_roles(db: Session = Depends(get_db)):
    result=roles_get(db)
    is_data = 1 if result else 0
    if result:
        role_list = []
        for user in result:
            role = {
                "id":user.id,
                "role_name": user.role_name,
                "permissions": user.permissions,
                "status": user.status
            }
            role_list.append(role)

        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
               "alert": [{
                    "message":common["SUCCESS_FETCHED_MSG"],# "Roles fetched successfully ",
                    "type": "Fetch"                    
                }],
                "users": role_list,
                "is_data":is_data
                
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "failure",
                "alert": [{
                    "message":common["NO_ROLE_MESSAGE"],# "No roles found",
                    "type": "failure"
                }],
                "is_data":is_data
            }
        }

@roles_router.put("/roles")
def update_role(role_id: str, role_data: UpdateRoleSchema, db: Session = Depends(get_db)):
    result = role_update(role_id, role_data, db)
    is_data = 1 if result else 0
    if result:
        roles_data = {
                    "role_name": result.role_name,
                    "permissions": result.permissions,
                    "status": result.status
                }
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["SUCCESS_UPDATED_MSG"],# f"Role updated successfully",
                    "type": "Update",
                }],
                "data": roles_data,
                "is_data":is_data
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "Failure",
                "alert": [{
                    "message":common["NO_ROLE_MESSAGE"],# "Role id not found, Or the Role already exists",
                    "type": "Failure"
                }],
                "is_data":is_data
            }
        }
    
@roles_router.delete("/roles")
def delete_role(role_id: str,db: Session = Depends(get_db)):

    result = role_delete(role_id, db)
    if result:
        return {
            "response": {
                "code": common["SUCCESS"],
                "status": "success",
                "alert": [{
                    "message":common["USER_DELETED"],# "Role deleted successfully",
                    "type": "deleted"
                }],
            }
        }
    else:
        return {
            "response": {
                "code": common["NOT_FOUND"],
                "status": "failure",
                "alert": [{
                    "message":common["NO_ROLE_MESSAGE"],# "Role not found",
                    "type": "failure"
                }],
            }
        }
