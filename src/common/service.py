from src.extensions import db
from src.permissions.models import ContentType
from .models import AutoRegisterModel


def register_all_models():
    with db.session.begin():
        for model_class in AutoRegisterModel.__subclasses__():
            register_model_event(model_class)


def register_model_event(model_class):
    table_name = model_class.__tablename__
    exists = ContentType.query.filter_by(table_name=table_name).first() is not None
    if not exists:
        new_entry = ContentType(table_name=table_name)
        db.session.add(new_entry)
