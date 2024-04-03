from datetime import datetime
from passlib.hash import bcrypt

from src.extensions import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def hash_password(self, password):
        self.password = bcrypt.hash(self.password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
