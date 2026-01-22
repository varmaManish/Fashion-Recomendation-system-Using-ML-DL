from flask import Blueprint, render_template, abort, request, session, redirect, url_for
from backend.utils.loaders import load_metadata, load_features
from backend.services.recommender import recommend_similar
from backend.auth.utils import login_required

pages_bp = Blueprint("pages", __name__)


# ---------------- HOME / SHOP ----------------
@pages_bp.route("/")
def home():
    meta = load_metadata()

    PER_PAGE = 30
    page = int(request.args.get("page", 1))

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE

    total_products = len(meta)
    total_pages = (total_products + PER_PAGE - 1) // PER_PAGE

    products = [
        {
            "id": idx,
            "name": row["filename"].replace(".jpg", ""),
            "image": row["filename"]
        }
        for idx, row in meta.iloc[start:end].iterrows()
    ]

    return render_template(
        "shop.html",
        products=products,
        page=page,
        total_pages=total_pages,
        cart_count=len(session.get("cart", []))
    )


# ---------------- PRODUCT PAGE ----------------
@pages_bp.route("/product/<int:product_id>")
def product_detail(product_id):
    meta = load_metadata()
    features = load_features()

    if product_id < 0 or product_id >= len(meta):
        abort(404)

    row = meta.iloc[product_id]

    product = {
        "id": product_id,
        "name": row["filename"].replace(".jpg", ""),
        "image": row["filename"]
    }

    query_vector = features[product_id]
    recommendations = recommend_similar(query_vector, top_k=8)

    return render_template(
        "product.html",
        product=product,
        recommendations=recommendations,
        cart_count=len(session.get("cart", []))
    )


# ---------------- AI SEARCH ----------------
@pages_bp.route("/ai-search")
def ai_search():
    return render_template("ai_search.html",cart_count=len(session.get("cart", []))
)


# ---------------- ADD TO CART (🔥 FIXED) ----------------
@pages_bp.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", [])

    cart.append(product_id)
    session["cart"] = cart
    session.modified = True

    # ✅ NO redirect
    return "", 204


# ---------------- CART ----------------
@pages_bp.route("/cart")
def cart():
    meta = load_metadata()
    cart_items = session.get("cart", [])

    products = []
    for pid in cart_items:
        if pid < len(meta):
            row = meta.iloc[pid]
            products.append({
                "id": pid,
                "name": row["filename"].replace(".jpg", ""),
                "image": row["filename"],
                "price": 999
            })

    return render_template(
        "cart.html",
        products=products,
        cart_count=len(cart_items)
    )


# ---------------- REMOVE FROM CART ----------------
@pages_bp.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)
        session["cart"] = cart
        session.modified = True

    return redirect(url_for("pages.cart"))


# ---------------- CHECKOUT ----------------
@pages_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    meta = load_metadata()
    cart_items = session.get("cart", [])

    if not cart_items:
        return redirect("/")

    products = []
    for pid in cart_items:
        if pid < len(meta):
            row = meta.iloc[pid]
            products.append({
                "id": pid,
                "name": row["filename"].replace(".jpg", ""),
                "price": 999
            })

    total = len(products) * 999

    return render_template(
        "checkout.html",
        products=products,
        total=total,
        cart_count=len(cart_items)
    )


# ---------------- PLACE ORDER ----------------
@pages_bp.route("/place-order", methods=["POST"])
@login_required
def place_order():
    session.pop("cart", None)
    return render_template("order_success.html", cart_count=0)


# ---------------- BUY NOW ----------------
@pages_bp.route("/buy-now/<int:product_id>", methods=["POST"])
@login_required
def buy_now(product_id):
    session["cart"] = [product_id]
    session.modified = True
    return redirect("/checkout")
@pages_bp.route("/cart-count")
def cart_count_api():
    return {"count": len(session.get("cart", []))}

