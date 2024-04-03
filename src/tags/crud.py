from src.extensions import db
from .models import Tag
from .exceptions import TagNotFound, TagAlreadyExists
from src.posts.models import Post


def get_tag_list():
    return Tag.query.all()


def get_tag_or_404(id):
    tag = Tag.query.get(id)
    if tag is None:
        raise TagNotFound
    return tag


def get_tag_by_name(name):
    tag = Tag.query.filter_by(name=name).first()
    if tag is not None:
        raise TagAlreadyExists


def create_tag(tag_data, post: Post):
    tag = Tag(**tag_data)
    post.tags.append(tag)
    db.session.add(tag)
    db.session.commit()
    return tag


def update_tag(tag):
    db.session.commit()
    return tag


def delete_tag(tag: Tag, post: Post):
    if tag in post.tags:
        post.tags.remove(tag)
        db.session.commit()

    if not tag.posts:
        db.session.delete(tag)
        db.session.commit()
