from flask import Blueprint, jsonify, request
from app.models import Habit
from app.database import db

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return "Brick by brick..."

@bp.route("/habits")
def get_habits():
    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return jsonify(
        [
            {
                "id": h.id,
                "name": h.name,
                "description": h.description,
                "created_at": h.created_at.isoformat() if h.created_at else None,
            }
            for h in habits
        ]
    )

@bp.route("/habits", methods=["POST"])
def make_habit():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    description = data.get("description")

    if not name:
        return jsonify({"Error": "name is required"}), 400

    habit = Habit(name=name, description=description)

    db.session.add(habit)
    db.session.commit()

    return (
        jsonify(
            {
                "id": habit.id,
                "name": habit.name,
                "description": habit.description,
                "created_at": habit.created_at.isoformat() if habit.created_at else None,
            }
        ),
        201,
    )
