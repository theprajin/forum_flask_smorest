from datetime import datetime
import enum

from src.extensions import db


class VoteType(enum.Enum):
    UP = 1
    DOWN = -1


class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content_type_id = db.Column(
        db.Integer, db.ForeignKey("content_types.id"), nullable=False
    )
    object_id = db.Column(db.Integer, nullable=False)
    vote_type = db.Column(db.Enum(VoteType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    content_type = db.relationship("ContentType", back_populates="votes")
    user = db.relationship("User", back_populates="votes")
