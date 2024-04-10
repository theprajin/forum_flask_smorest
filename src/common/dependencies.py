from functools import wraps
from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from src.permissions.models import ContentType
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


def permission_required(
    resource_type,
    can_read=False,
    can_write=False,
    can_modify=False,
    can_delete=False,
):
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            user = g.get("current_user")
            g.has_permission = False

            if user is None:
                raise UnauthorizedAccess("Unauthorized Access")

            if user.is_superuser:
                g.has_permisssion = True
                return fn(*args, **kwargs)

            user_permissions = {
                permission.content_type_id: permission
                for role in user.roles
                for permission in role.permissions
            }

            for permission in user_permissions.values():
                if (
                    ContentType.query.get(permission.content_type_id).table_name
                    == resource_type
                ):
                    if (
                        (can_read and permission.can_read)
                        or (can_write and permission.can_write)
                        or (can_modify and permission.can_modify)
                        or (can_delete and permission.can_delete)
                    ):
                        g.has_permission = True
                        return fn(*args, **kwargs)

            else:
                raise UnauthorizedAccess("Unauthorized Access")

        return wrapped

    return wrapper
