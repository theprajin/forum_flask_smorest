from src.extensions import db


def create_post_view(post_view):
    db.session.add(post_view)
    db.session.commit()
    return post_view
