""" Utility """
from flask import session
from databus.client.user import Role

def get_authorization() -> dict:
    """ Returns authorization state """
    user_root = "client_id" in session and session["client_id"] == "root"
    user_admin = "user_role" in session and session["user_role"] == Role.ADMINISTRATOR.name
    return {
        "user_is_root": user_root,
        "user_is_admin": user_admin
    }

def user_is_admin() -> bool:
    """ Returns true if user is admin """
    return get_authorization()["user_is_admin"]
