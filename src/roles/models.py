from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class Role(AutoRegisterModel):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    permissions = db.relationship(
        "Permisssion",
        secondary="role_permission",
        back_populates="roles",
        cascade="all, delete",
    )
    users = db.relationship(
        "User",
        secondary="user_role",
        back_populates="roles",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return self.name


# assiciation table for roles and permissions
role_permission_table = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "permission_id", db.Integer, db.ForeignKey("permissions.id"), primary_key=True
    ),
)
