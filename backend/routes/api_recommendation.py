from flask import Blueprint, request, jsonify
from PIL import Image

from backend.services.feature_extractor import extract_feature
from backend.services.recommender import recommend_similar

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/recommend", methods=["POST"])
def recommend():
    """
    Real AI-powered recommendation endpoint
    """

    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Load image
        image = Image.open(file).convert("RGB")

        # 1. Extract feature vector
        query_vector = extract_feature(image)

        # 2. Get similar products
        recommendations = recommend_similar(query_vector, top_k=8)

        return jsonify({
            "status": "success",
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
