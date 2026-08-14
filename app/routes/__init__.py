from .auth import auth_bp
from .user import user_bp
from .admin import admin_bp
from .image import image_bp
from .ml import ml_bp
from .dataset import dataset_bp
from .annotation import annotation_bp

__all__ = ["auth_bp", "user_bp", "admin_bp", "image_bp", "ml_bp", "dataset_bp", "annotation_bp"]
