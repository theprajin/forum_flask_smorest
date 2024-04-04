from functools import wraps
from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from src.users.models import User
from .exceptions import UnauthorizedAccess


def load_user_from_request(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            g.current_user = user
            return fn(*args, **kwargs)
        except Exception as e:
            raise UnauthorizedAccess

    return wrapper
