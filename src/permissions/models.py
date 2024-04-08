from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class ContentType(db.Model):
    __tablename__ = "content_types"
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)
    permissions = db.relationship(
        "Permisssion", back_populates="content_type", cascade="all, delete"
    )
    votes = db.relationship(
        "Vote", back_populates="content_type", cascade="all, delete"
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __str__(self):
        return self.name


class Permisssion(AutoRegisterModel):
    __tablename__ = "permissions"
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=False)
    content_type_id = db.Column(
        db.Integer, db.ForeignKey("content_types.id"), nullable=False
    )
    content_type = db.relationship(
        "ContentType", back_populates="permissions", cascade="all, delete"
    )
    roles = db.relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return self.name
