from flask_smorest import abort
from src.extensions import db
from .models import Post
from .exceptions import PostNotFound


def get_post_list():
    return Post.query.all()


def get_post_or_404(id):
    post = Post.query.get(id)
    if post is None:
        raise PostNotFound
    return post


def create_post(post_data, user_id):
    post = Post(**post_data)
    post.user_id = user_id
    db.session.add(post)
    db.session.commit()
    return post


def update_post(post):
    db.session.commit()
    return post


def delete_post(id):
    try:
        Post.query.filter(Post.id == id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e)
