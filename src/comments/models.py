from datetime import datetime
from src.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now()
    )

    def __str__(self):
        return f"<Comment {self.content}>"
