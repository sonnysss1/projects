from multiprocessing import Value
from flask import Blueprint, jsonify, request, render_template, url_for, redirect, flash
from app.models import Habit
from app.database import db

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return render_template("index.html", habits=habits)


@bp.route("/habits/add", methods=["GET","POST"])
def add_habit():

    if request.method == "POST":
        name = (request.form.get("name")).strip()
        description = (request.form.get("description"))

        if not name:
            flash("A name is required.", "error")
            return redirect(url_for("add_habit.html"))

        try:
            habit = Habit(name=name, description=description)
            db.session.add(habit)
            db.session.commit()
            flash("Habit added successfully!", "success")
        except ValueError as e:
            flash(str(e), "error")
            return render_template("add_habit.html")

        return redirect(url_for("main.home"))

    return render_template("add_habit.html")



@bp.route("/habits/<int:id>/edit", methods=["GET", "POST"])
def edit_habit(id):
    habit = Habit.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "")


        try:
            if name:
                habit.name = name

            habit.description = description
            db.session.commit()
            flash("Habit has been updated!", "success")
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "error")
            #stay on the edit page if error occurs
            return render_template("edit.html", habit=habit)    

        return redirect(url_for("main.home"))

    return render_template("edit.html", habit=habit)


@bp.route("/habits/<int:id>/delete", methods=["GET", "POST"])
def delete_habit(id):
    habit = Habit.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(habit)
        db.session.commit()
        flash("Habit has been deleted!", "success")
        return redirect(url_for("main.home"))

    return render_template("delete.html", habit=habit)