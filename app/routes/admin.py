from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from app.models.user import User
from app.models.category import Category
from app.models.image import Image
from app.extensions import db

admin_bp = Blueprint("admin", __name__)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != "admin":
            return jsonify({"message": "Admin privileges required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route("/categories", methods=["GET", "POST"])
@jwt_required()
@admin_required
def manage_categories():
    if request.method == "POST":
        data = request.get_json()
        if not data or not data.get("class_name") or data.get("class_code") is None:
            return jsonify({"message": "Missing class_name or class_code"}), 400
        
        if Category.query.filter_by(class_name=data["class_name"]).first():
            return jsonify({"message": "Category already exists"}), 409

        new_category = Category(
            class_name=data["class_name"],
            class_code=data["class_code"]
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created", "category_id": new_category.category_id}), 201

    # GET method
    categories = Category.query.all()
    results = [{"id": c.category_id, "name": c.class_name, "code": c.class_code, "validated_count": c.validated_count} for c in categories]
    return jsonify({"categories": results}), 200


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    users = User.query.all()
    results = [{
        "user_id": u.user_id,
        "email": u.email,
        "role": u.role,
        "image_count": u.image_count,
        "reward_points": u.reward_points
    } for u in users]
    return jsonify({"users": results}), 200


@admin_bp.route("/validation-queue", methods=["GET"])
@jwt_required()
@admin_required
def get_validation_queue():
    images = Image.query.filter_by(status="uploaded", is_validated=False).all()
    results = [{
        "image_id": img.image_id,
        "original_filename": img.original_filename,
        "uploaded_at": img.uploaded_at
    } for img in images]
    return jsonify({"queue": results}), 200


@admin_bp.route("/images/<image_id>/approve", methods=["POST"])
@jwt_required()
@admin_required
def approve_image(image_id):
    data = request.get_json() or {}
    action = data.get("action") # 'approve' or 'reject'
    
    img = Image.query.get(image_id)
    if not img:
        return jsonify({"message": "Image not found"}), 404
        
    if action == "approve":
        img.status = "approved"
        img.is_validated = True
        
        # Award credits to uploader
        uploader = User.query.get(img.user_id)
        if uploader and not img.reward_given:
            uploader.reward_points += 10 # Example fixed points
            uploader.image_count += 1
            img.reward_given = True
            img.credits_awarded = 10
            
    elif action == "reject":
        img.status = "rejected"
        img.is_validated = True
    else:
        return jsonify({"message": "Invalid action. Use 'approve' or 'reject'"}), 400

    db.session.commit()
    return jsonify({"message": f"Image {action}d successfully"}), 200
