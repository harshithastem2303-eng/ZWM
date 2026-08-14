from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.models.image import Image

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "user_id": user.user_id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_email_verified": user.is_email_verified,
        "reward_points": user.reward_points,
        "image_count": user.image_count,
        "created_at": user.created_at
    }), 200


@user_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    validated_images = Image.query.filter_by(user_id=current_user_id, is_validated=True).count()
    total_images = Image.query.filter_by(user_id=current_user_id).count()

    return jsonify({
        "total_uploads": total_images,
        "validated_images": validated_images,
        "pending_images": total_images - validated_images,
        "reward_points": user.reward_points
    }), 200


@user_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    current_user_id = get_jwt_identity()
    images = Image.query.filter_by(user_id=current_user_id).order_by(Image.uploaded_at.desc()).all()
    
    results = []
    for img in images:
        results.append({
            "image_id": img.image_id,
            "original_filename": img.original_filename,
            "status": img.status,
            "is_validated": img.is_validated,
            "credits_awarded": img.credits_awarded,
            "uploaded_at": img.uploaded_at
        })

    return jsonify({"history": results}), 200


@user_bp.route("/rewards", methods=["GET"])
@jwt_required()
def get_rewards():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "reward_points": user.reward_points,
        "total_images_contributed": user.image_count
    }), 200
