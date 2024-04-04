from datetime import datetime
from src.extensions import db
from src.common.models import AutoRegisterModel


post_tag_table = db.Table(
    "post_tag",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Tag(AutoRegisterModel):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    posts = db.relationship(
        "Post",
        secondary=post_tag_table,
        back_populates="tags",
        cascade="all, delete",
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return self.name
