from flask import Blueprint, jsonify

dataset_bp = Blueprint("dataset", __name__)

@dataset_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "dataset"}), 200
