from src.extensions import db
from .models import Category
from .exceptions import CategoryNotFound, CategoryAlreadyExists


def get_category_list():
    categories = Category.query.all()
    return categories


def get_category_or_404(category_id):
    category = Category.query.get(category_id)
    if not category:
        raise CategoryNotFound
    return category


def get_category_by_name(name):
    category = Category.query.filter_by(name=name).first()
    if category is not None:
        raise CategoryAlreadyExists


def create_category(category_data):
    category = Category(**category_data)
    db.session.add(category)
    db.session.commit()
    return category


def update_category(category):
    db.session.commit()
    return category


def delete_category(category_id):
    Category.query.filter(Category.id == category_id).delete()
    db.session.commit()
