from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import uuid

from app.models.user import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing email or password"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 409

    hashed_password = generate_password_hash(data["password"])
    verification_token = str(uuid.uuid4())

    new_user = User(
        email=data["email"],
        password_hash=hashed_password,
        full_name=data.get("full_name", ""),
        verification_token=verification_token,
    )

    db.session.add(new_user)
    db.session.commit()

    # Mock email sending for verification
    print(f"Mock sending email to {new_user.email} with token: {verification_token}")

    return jsonify({"message": "User registered successfully", "user_id": new_user.user_id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user.user_id,
        "role": user.role
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # To fully implement logout, we'd need to blacklist the token.
    # For now, we rely on the client removing the token.
    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    if not data or not data.get("email"):
        return jsonify({"message": "Missing email"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user:
        reset_token = str(uuid.uuid4())
        # Normally save token to user model or token table with expiry
        # Mocking for now
        print(f"Mock sending reset email to {user.email} with token: {reset_token}")
        
    # Always return a generic message to prevent user enumeration
    return jsonify({"message": "If the email is registered, a password reset link has been sent"}), 200

