from flask import Flask
from backend.auth.routes import auth_bp
from dotenv import load_dotenv
import os


def create_app():
    """
    Application factory.
    Creates and configures the Flask app.
    """
    load_dotenv()
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    # Basic config (we'll harden this later)
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.secret_key = os.getenv("FLASK_SECRET_KEY")


    # --- Register Blueprints (routes) ---
    # NOTE: these files don't exist yet.
    # We will create them step-by-step.
    from backend.routes.pages import pages_bp
    from backend.routes.api_recommendation import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)

    return app
