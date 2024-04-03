from src.extensions import db
from .models import User
from .exceptions import UserNotFound, UserAlreadyExists


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        raise UserNotFound
    return user


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is not None:
        raise UserAlreadyExists
    return user


def check_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise UserNotFound
    return user


def create_user(user_data):
    user = User(**user_data)
    user.hash_password(user.password)
    db.session.add(user)
    db.session.commit()
    return user
