from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


class Thread(AutoRegisterModel):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="threads")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return f"<Thread {self.id}>"
