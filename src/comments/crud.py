from src.extensions import db
from .models import Comment
from .exceptions import CommentNotFound


def get_comment_list():
    comments = Comment.query.all()
    return comments


def get_comment_or_404(id):
    comment = Comment.query.get(id)
    if comment is None:
        raise CommentNotFound
    return comment


def create_comment(comment_data):
    comment = Comment(**comment_data)
    db.session.add(comment)
    db.session.commit()
    return comment


def update_comment(comment):
    db.session.commit()
    return comment


def delete_comment(id):
    Comment.query.filter(Comment.id == id).delete()
    db.session.commit()
