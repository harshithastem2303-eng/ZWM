import uuid
from datetime import datetime, timezone

from app.extensions import db


class TrainingJob(db.Model):
    __tablename__ = "training_jobs"

    job_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version = db.Column(db.String(20), nullable=False)
    class_counts = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(20), default="queued")
    best_model_path = db.Column(db.Text, nullable=True)
    metadata_path = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    model_versions = db.relationship("ModelVersion", backref="training_job", lazy=True)


class ModelVersion(db.Model):
    __tablename__ = "model_versions"

    model_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = db.Column(db.String(36), db.ForeignKey("training_jobs.job_id"), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    is_current = db.Column(db.Boolean, default=False)
    map_score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )