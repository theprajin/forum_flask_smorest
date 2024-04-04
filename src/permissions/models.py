from datetime import datetime
from src.extensions import db


class ContentType(db.Model):
    __tablename__ = "content_types"
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __str__(self):
        return self.name


class Permisssion(db.Model):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return self.name
