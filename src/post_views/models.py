from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class PostView(AutoRegisterModel):
    __tablename__ = "post_views"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user = db.relationship("User", back_populates="views")
    post = db.relationship("Post", back_populates="views")

    def __str__(self):
        return f"{self.post_id} - {self.user_id}"
