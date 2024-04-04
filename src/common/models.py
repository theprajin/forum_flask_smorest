from src.extensions import db


class AutoRegisterModel(db.Model):
    __abstract__ = True
