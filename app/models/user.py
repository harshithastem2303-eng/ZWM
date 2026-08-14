import uuid
from datetime import datetime, timezone

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    role = db.Column(db.String(20), default="user")
    is_email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.Text, nullable=True)
    reward_points = db.Column(db.Integer, default=0)
    image_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    images = db.relationship("Image", backref="user", lazy=True, cascade="all, delete-orphan")
    annotations = db.relationship("Annotation", backref="annotator", lazy=True)


class Admin(db.Model):
    __tablename__ = "admins"

    admin_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    admin_name = db.Column(db.String(150), nullable=False)
    admin_email = db.Column(db.String(30), unique=True, nullable=False)
    is_email_verified = db.Column(db.Boolean, default=False)
    hash_password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )