from flask import Flask
from backend.auth.routes import auth_bp
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static"
    )

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    app.secret_key = app.config["SECRET_KEY"]

    # Blueprints
    from backend.routes.pages import pages_bp
    from backend.routes.api_recommendation import api_bp
    from backend.routes.api_web_search import web_search_bp   

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(web_search_bp)                      

    return app