import os
from datetime import timedelta


class Config:
    """Base configuration for the application."""

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/zwm_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", "zwm-bucket")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    CATEGORY_VALIDATED_THRESHOLD = int(os.getenv("CATEGORY_VALIDATED_THRESHOLD", 100))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
