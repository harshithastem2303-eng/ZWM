from flask import Blueprint, jsonify


ml_bp = Blueprint("ml", __name__)


@ml_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "ml"}), 200
