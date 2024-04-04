from src.extensions import db
from .models import User


def create_super_user(user: User):
    total_user = User.query.count()

    if total_user <= 0:
        user.is_superuser = True
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
