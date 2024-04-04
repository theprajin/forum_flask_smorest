from src.extensions import db
from .models import Role
from .exceptions import RoleNotFound


def get_role_list():
    return Role.query.all()


def get_role_or_404(id):
    role = Role.query.get(id)
    if role is None:
        raise RoleNotFound
    return role


def create_role(role_data):
    role = Role(**role_data)
    db.session.add(role)
    db.session.commit()
    return role


def update_role(role):
    db.session.commit()
    return role


def delete_role(id):
    Role.query.filter(Role.id == id).delete()
    db.session.commit()
