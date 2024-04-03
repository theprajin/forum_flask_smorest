from datetime import datetime
from src.extensions import db
from src.tags.models import post_tag_table


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref="post", lazy="dynamic")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    tags = db.relationship(
        "Tag",
        secondary=post_tag_table,
        back_populates="posts",
        cascade="all, delete",
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self) -> str:
        return f"<Post {self.title}>"
