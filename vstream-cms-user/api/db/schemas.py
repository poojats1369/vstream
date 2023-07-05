from pydantic import BaseModel, constr, EmailStr, validator
from fastapi import HTTPException
from typing import List
from enum import Enum


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]com$'
# pass_regex='((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})' 

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

class AllowedRoles(str, Enum):
    VALUE1 = "super_admin"
    VALUE2 = "admin"
    VALUE3 = "editor"
    VALUE4 = "author"
    VALUE5 = "subscriber"

class CmsBase(BaseModel):
    first_name: str
    last_name: str = None
    email: str #constr(regex=regex)
    emp_id: str = None
    password: str #constr(regex=pass_regex)
    role:str
    phone: str #constr(regex=r'^\d{10}$')

class CmsUpdate(BaseModel):
    first_name: str
    last_name: str = None
    email: str 
    emp_id: str = None
    role: str
    phone:  str 

class CmsLogin(BaseModel):
    email: constr(regex=regex)
    password: str 

class CmsUpdatePassword(BaseModel):
    password: str 

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

class RoleSchema(BaseModel):
    role_name: constr(
        strip_whitespace=True,
        to_lower=True,
        regex=f"({'|'.join(v.value for v in AllowedRoles)})",
    )
    permissions: List[str]
    status: bool

    @validator('role_name')
    def validate_role(cls, value):
        if value not in [v.value for v in AllowedRoles]:
            raise ValueError(f"Invalid value. Allowed values are {', '.join(v.value for v in AllowedRoles)}.")
        return value

class UpdateRoleSchema(BaseModel):
    permissions: List[str]
    status: bool

class PermissionSchema(BaseModel):
   permission_name: str
   permission_type: str 
   collection: List[str]
   status: bool

class UpdateStatusSchema(BaseModel):
    user_id :str
    is_active:bool 
    role: str 

class OTPRequest(BaseModel):
    phone_number: str

class UserActivityLogSchema(BaseModel):
    user_role: str
    user_id: int
    activity_slug: str 
    logged_at: str 


class UserActivityListSchema(BaseModel):
    activity_name: str 
    activity_description:str
    activity_slug: str 
    status: bool 

class UserActivityIDSchema(BaseModel):
    user_id : str
    user_role : str
    activity_id : str
    activity_slug : str
    logged_at : str
    activity_name : str
    activity_description : str

class UserActivitySchema(BaseModel):
    activity_name : str
    activity_description : str
	

