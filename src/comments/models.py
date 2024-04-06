from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class Comment(AutoRegisterModel):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    threads = db.relationship("Thread", backref="comment", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="comments")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return f"<Comment {self.id}>"
