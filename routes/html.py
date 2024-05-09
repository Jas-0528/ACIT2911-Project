import random
from flask import Blueprint, render_template, request
from sqlalchemy.sql import functions as func
from db import db
from models import Question

html_bp = Blueprint("html", __name__)


# Homepage
@html_bp.route("/", methods=["GET"])
def home():
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("home.html", random_id=random_id)


# Game page
@html_bp.route("/play/<int:question_id>", methods=["GET"])
def play_question(question_id):
    # Retrieve question from database based on id in URL
    question_obj = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    # Generate random id for next question button
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    # Create dictionary to be passed to Flask template
    question_data = question_obj.to_dict()
    question_data.update(
        {
            "answers": question_obj.incorrect_answers + [question_obj.correct_answer],
            "random_id": random_id,
            "answered": False,
            "correct": False,
        }
    )
    return render_template("play.html", **question_data)


# Game page post
@html_bp.route("/play/<int:question_id>", methods=["POST"])
def play_question_submit(question_id):
    # Retrieve user-submited answer
    answer = request.form.get("answer")
    # Retrieve question from database based on id in URL
    question_obj = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    # Create dictionary to be passed to Flask template
    question_data = question_obj.to_dict()
    question_data.update(
        {
            "answers": question_obj.incorrect_answers + [question_obj.correct_answer],
            "random_id": random_id,
            "answered": True,
            "correct": False,
        }
    )
    if question_obj.correct_answer == answer:
        # If user-submitted answer is correct
        question_data["correct"] = True
        return render_template("play.html", **question_data)
    else:
        # If user-submitted answer is incorrect
        return render_template("play.html", **question_data)
