from app.extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(25), unique=True, nullable=False)
    class_code = db.Column(db.Integer, unique=True, nullable=False)
    validated_count = db.Column(db.Integer, default=0)

    annotations = db.relationship("Annotation", backref="category", lazy=True)