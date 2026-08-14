from flask import Flask

from .config import Config, config
from .extensions import db, jwt, migrate


def create_app(config_name: str = "default"):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes import admin_bp, auth_bp, image_bp, ml_bp, user_bp, dataset_bp, annotation_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/user")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(image_bp, url_prefix="/api/images")
    app.register_blueprint(ml_bp, url_prefix="/api/ml")
    app.register_blueprint(dataset_bp, url_prefix="/api/dataset")
    app.register_blueprint(annotation_bp, url_prefix="/api/annotations")

    return app