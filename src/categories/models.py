from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class Category(AutoRegisterModel):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    posts = db.relationship("Post", backref="category", lazy="dynamic")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return f"<Category {self.name}>"
