import uuid
from datetime import datetime, timezone

from app.extensions import db


class Annotation(db.Model):
    __tablename__ = "annotations"

    annotation_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id = db.Column(db.String(36), db.ForeignKey("images.image_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    annotated_by = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    label_json_path = db.Column(db.Text, nullable=True)
    yolo_label_path = db.Column(db.Text, nullable=True)
    annotated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))