from api.db import *
from utils import *
from utils.constants import common
from fastapi import Depends
from api.helper.helper import *
from sqlalchemy.orm import Session


def user_activity_funct(request_1: UserActivityLogSchema, request_2: UserActivityListSchema, db: Session = Depends(get_db)):
    valid_user_roles = ["super_admin", "admin", "editor", "author", "subscriber"]

    if request_1.user_role.lower() not in valid_user_roles:
        # return {"success": False, "message": common['FAILURE_MSG']}
        return {"success": False, "message": common['INVALID_ROLE']}
    activity_id=uuid.uuid4().hex
    if valid_user_roles:
        user_activity_list = UserActivityList(
            activity_name=request_2.activity_name,
            activity_description=request_2.activity_description,
            activity_slug=request_2.activity_slug,
            activity_id=activity_id,
            status=request_2.status
        )

        user_activity_log = UserActivityLog(
            user_role=request_1.user_role,
            activity_id=activity_id,
            user_id=request_1.user_id,
            activity_slug=request_1.activity_slug,
            logged_at=request_1.logged_at
        )

        db.add(user_activity_list)
        db.add(user_activity_log)
        db.commit()

        return {"success": True}
    else:
        return {"success": False}

def get_user_by_activity_id(activity_id,db):

    activities = db.query(UserActivityLog).filter(UserActivityLog.activity_id == activity_id).all()
    if activities:
        result = []
        for activity in activities:
            result.append({
                "id": activity.id,
                "user_id": activity.user_id,
                "user_role": activity.user_role,
                "activity_id": activity.activity_id,
                "activity_slug": activity.activity_slug,
                "logged_at": activity.logged_at,
                "activity_name": activity.activity.activity_name,
                "activity_description": activity.activity.activity_description
            })
        return {"success": True, "activity":result}
    else:
        return {"success": False}

def get_all_activities(db):
    activities = db.query(UserActivityLog, UserActivityList).all()
    if activities:
        result = []
        for activity in activities:
            result.append({
                "id": activity.id,
                "user_id": activity.user_id,
                "user_role": activity.user_role,
                "activity_id": activity.activity_id,
                "activity_slug": activity.activity_slug,
                "logged_at": activity.logged_at,
                "activity_name": activity.activity.activity_name,
                "activity_description": activity.activity.activity_description
            })
        return {"success": True, "activities": result}
    else:
        return {"success": False}


def get_all_user_activity(db):
    activities = db.query(UserActivityLog).join(UserActivityList, UserActivityList.activity_id == UserActivityLog.activity_id).all()

    if activities:
        result = []
        for activity in activities:
            result.append({
                "id": activity.id,
                "user_id": activity.user_id,
                "user_role": activity.user_role,
                "activity_id": activity.activity_id,
                "activity_slug": activity.activity_slug,
                "logged_at": activity.logged_at,
                "activity_name": activity.activity.activity_name,
                "activity_description": activity.activity.activity_description
            })
        return {"success": True, "activities": result}
    else:
        return {"success": False}
        

