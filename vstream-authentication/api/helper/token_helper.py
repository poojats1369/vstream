from api.db import *
from jose import jwt
from utils import *
from datetime import  timedelta

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    CURRENT_TIME = get_current_time()  # Update the current time

    to_encode = data.copy()
    if expires_delta:
        expire = CURRENT_TIME + expires_delta
    else:
        expire = CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KET, ALGORITHM)
    return encoded_jwt