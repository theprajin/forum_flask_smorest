from datetime import datetime
from src.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now()
    )

    def __str__(self) -> str:
        return f"<Post {self.title}>"
