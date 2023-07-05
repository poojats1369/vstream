from api.db import *
from utils import *
from api.helper import *
from sqlalchemy import update
from datetime import timedelta




def refresh_token_fun(refresh_token, db):
    CURRENT_TIME = get_current_time()  # Update the current time

    # Retrieve the user's record from the Token table
    token = db.query(Token).filter(Token.refresh_token == refresh_token).first()

    if not token:
        return {"success": False, "code": common['NOT_FOUND'],  "message": common['NO_USER_MESSAGE']}

    # Generate a new access token
    new_access_token = create_access_token({"user_id": token.user_id})

    stmt = update(Token).where(Token.refresh_token == refresh_token).values(
        access_token=new_access_token,
        at_updated=CURRENT_TIME,
        at_expiry=CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME)
    )
    db.execute(stmt)
    db.commit()

    expiry_time = (CURRENT_TIME + timedelta(hours=ACCESS_TOKEN_EXPIRE_TIME))
    formatted_expiry = expiry_time.strftime("%d/%m/%Y")

    return {
        "success": True,
        "access_token": new_access_token,
        "at_expiry": formatted_expiry,
        "expires_in": f"{ACCESS_TOKEN_EXPIRE_TIME} hrs " 
    }
