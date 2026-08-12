from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "portfolio-demo-secret-change-me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ecommerce.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes import web
    from .api import api
    app.register_blueprint(web)
    app.register_blueprint(api, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
