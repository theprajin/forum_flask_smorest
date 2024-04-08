from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel
from src.tags.models import post_tag_table


class Post(AutoRegisterModel):
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
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="posts")
    views = db.relationship("PostView", back_populates="post")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    voteable = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self) -> str:
        return f"<Post {self.title}>"
