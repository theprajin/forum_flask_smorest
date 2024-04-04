from src.extensions import db
from .models import Permisssion, ContentType
from .exceptions import PermissionNotFound


def get_content_type_list():
    return db.session.query(ContentType).all()


def get_content_type_or_404(id):
    content_type = ContentType.query.get(id)
    if content_type is None:
        raise PermissionNotFound
    return content_type


def get_permission_list():
    return db.session.query(Permisssion).all()


def get_permission_or_404(id):
    permission = Permisssion.query.get(id)
    if permission is None:
        raise PermissionNotFound
    return permission


def create_permission(permission_data):
    permission = Permisssion(**permission_data)
    db.session.add(permission)
    db.session.commit()
    return permission


def update_permission(permission):
    db.session.commit()
    return permission


def delete_permission(id):
    Permisssion.query.filter(Permisssion.id == id).delete()
    db.session.commit()
