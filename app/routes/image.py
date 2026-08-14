from flask import Blueprint, jsonify


image_bp = Blueprint("image", __name__)


@image_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "image"}), 200
