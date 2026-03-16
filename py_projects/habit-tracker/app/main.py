from multiprocessing import Value
from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
from app.models import Habit
from app.database import db

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return render_template("index.html", habits=habits)


@bp.route("/habits/add", methods=["POST"])
def add_habit_form():
    name = (request.form.get("name")).strip()
    description = (request.form.get("description"))

    if not name:
        return redirect(url_for("main.home"))

    try:
        habit = Habit(name=name, description=description)
        db.session.add(habit)
        db.session.commit()
        flash("Habit added successfully!", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("main.home"))

@bp.route("/habits/<int:id>/edit", methods=["GET", "POST"])
def edit_habit(id):
    habit = Habit.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "")

        if name:
            habit.name = name

        try:
            habit.description = description
            db.session.commit()
            flash("Edited habit successfully!", "success")
        except ValueError as e:
            flash(str(e), "error")

        return redirect(url_for("main.home"))

    return render_template("edit.html", habit=habit)


@bp.route("/habits/<int:id>/delete", methods=["POST"])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)
    db.session.delete(habit)
    db.session.commit()
    return redirect(url_for("main.home"))