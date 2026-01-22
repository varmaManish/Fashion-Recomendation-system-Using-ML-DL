from flask import Blueprint, render_template, request, redirect, session, flash
from backend.db import users_collection
from backend.auth.utils import hash_password, check_password

auth_bp = Blueprint("auth", __name__)

# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if users_collection.find_one({"email": email}):
            flash("User already exists. Please login.", "error")
            return redirect("/login")

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hash_password(password)
        })

        flash("Registration successful! Please login.", "success")
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users_collection.find_one({"email": email})

        if not user or not check_password(password, user["password"]):
            flash("Invalid email or password", "error")
            return redirect("/login")

        # SUCCESS
        session["user_id"] = str(user["_id"])
        session["user_email"] = user["email"]
        session["user_name"] = user["name"]

        flash(f"Welcome back, {user['name']}!", "success")

        # 🔥 redirect back if user was forced to login
        next_page = request.args.get("next")
        return redirect( next_page or "shop.html")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/")
