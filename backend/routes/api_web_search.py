"""
backend/routes/api_web_search.py
─────────────────────────────────────────────────────────────
Google Lens visual search via SerpAPI.

Flow:
  1. User POSTs an image file
  2. We upload it to imgbb (free, public URL)
  3. We hit SerpAPI Google Lens with type=products
  4. Return top-10 product matches from real e-commerce sites
     (Amazon, Flipkart, Myntra, etc.)

ENV variables needed (.env):
  SERPAPI_KEY    = your SerpAPI key   (https://serpapi.com)
  IMGBB_API_KEY  = your imgbb API key (https://api.imgbb.com)
"""

import os
import base64
import requests
from flask import Blueprint, request, jsonify
from PIL import Image
import io

web_search_bp = Blueprint("web_search", __name__, url_prefix="/api")

# ── helpers ────────────────────────────────────────────────

def _upload_to_imgbb(image_bytes: bytes) -> str:
    """Upload raw image bytes to imgbb and return a public URL."""
    api_key = os.getenv("IMGBB_API_KEY")
    if not api_key:
        raise EnvironmentError("IMGBB_API_KEY not set in .env")

    b64 = base64.b64encode(image_bytes).decode("utf-8")
    resp = requests.post(
        "https://api.imgbb.com/1/upload",
        params={"key": api_key},
        data={"image": b64},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"imgbb upload failed: {data}")
    return data["data"]["url"]           # public https:// URL


def _google_lens_search(image_url: str, top_k: int = 10) -> list:
    """Call SerpAPI Google Lens and return top_k product results."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise EnvironmentError("SERPAPI_KEY not set in .env")

    params = {
        "engine": "google_lens",
        "url": image_url,
        "type": "products",          # focuses on shoppable results
        "api_key": api_key,
        "hl": "en",
        "country": "in",             # India → surfaces Flipkart / Myntra results
    }

    resp = requests.get("https://serpapi.com/search", params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    # SerpAPI returns visual_matches or products depending on type
    raw = data.get("visual_matches") or data.get("products_results") or []

    results = []
    for item in raw[:top_k]:
        price_info = item.get("price", {})
        results.append({
            "title":       item.get("title", "Fashion Item"),
            "link":        item.get("link", "#"),
            "source":      item.get("source", ""),
            "source_icon": item.get("source_icon", ""),
            "thumbnail":   item.get("thumbnail", ""),
            "price":       price_info.get("value", ""),
            "rating":      item.get("rating"),
            "reviews":     item.get("reviews"),
            "in_stock":    item.get("in_stock", True),
        })

    return results


# ── route ──────────────────────────────────────────────────

@web_search_bp.route("/web-search", methods=["POST"])
def web_search():
    """
    POST /api/web-search
    Form-data: image (file)
    Returns: JSON with top-10 web product matches
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        # 1. Read & validate image
        image_bytes = file.read()
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Re-encode as JPEG for smaller upload
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        jpeg_bytes = buf.getvalue()

        # 2. Upload to imgbb → public URL
        public_url = _upload_to_imgbb(jpeg_bytes)

        # 3. Google Lens search via SerpAPI
        products = _google_lens_search(public_url, top_k=10)

        return jsonify({
            "status": "success",
            "image_url": public_url,
            "web_results": products,
            "total": len(products),
        })

    except EnvironmentError as e:
        return jsonify({"status": "error", "message": str(e)}), 503
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500