from functools import wraps
from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from src.users.models import User
from .exceptions import UnauthorizedAccess


def load_user_from_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user is None:
            raise UnauthorizedAccess("User not found")
        g.current_user = user
        return fn(*args, **kwargs)

    return wrapper


def superuser_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = g.get("current_user")
        # print(f"user is {user}")

        if user is None:
            raise UnauthorizedAccess("Unauthorized Access")
        if user.is_superuser:
            return fn(*args, **kwargs)
        else:
            raise UnauthorizedAccess("Unauthorized Access")

    return wrapper
