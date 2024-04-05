from src.extensions import db


class TokenBlockList(db.Model):
    __tablename__ = "blocklist"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, unique=True)
