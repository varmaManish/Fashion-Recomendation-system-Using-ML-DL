from flask_bcrypt import Bcrypt
from functools import wraps
from flask import session, redirect, request

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode("utf-8")

def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login?next=" + request.path)
        return view(*args, **kwargs)
    return wrapped_view
