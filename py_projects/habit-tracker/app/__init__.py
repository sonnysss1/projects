import os
from flask import Flask
from app.main import bp
from app.database import db
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///habit_tracker.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-only-fallback")

    db.init_app(app)

    app.register_blueprint(bp)
    with app.app_context():
        db.create_all()
    return app
