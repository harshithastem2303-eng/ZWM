from flask import Blueprint, jsonify

annotation_bp = Blueprint("annotation", __name__)

@annotation_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "annotation"}), 200
