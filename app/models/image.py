import uuid
from datetime import datetime, timezone

from app.extensions import db


class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    temp_s3_path = db.Column(db.Text, nullable=True)
    permanent_s3_path = db.Column(db.Text, nullable=True)
    split_type = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(30), default="uploaded")
    is_validated = db.Column(db.Boolean, default=False)
    reward_given = db.Column(db.Boolean, default=False)
    credits_awarded = db.Column(db.Integer, default=0)
    uploaded_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    validated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    annotations = db.relationship("Annotation", backref="image", lazy=True, cascade="all, delete-orphan")