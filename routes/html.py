import json
from flask import Blueprint, render_template, request
from sqlalchemy.sql import functions as func
from db import db
from models import Question

html_bp = Blueprint("html", __name__)


# Homepage
@html_bp.route("/", methods=["GET"])
def home():
    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    return render_template("home.html", next_question_id=random_question_id)


# Play random page
@html_bp.route("/play/<int:question_id>", methods=["GET"])
def play_random(question_id):
    # Retrieve question from database based on id in URL
    question = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    # Generate random id for next question button
    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    # Create dictionary to be passed to Flask template
    question_data = question.to_dict()
    question_data.update(
        {
            "answers": json.loads(question.incorrect_answers_string)
            + [question.correct_answer],
            "next_question_id": random_question_id,
            "answered": False,
            "correct": False,
        }
    )
    return render_template("play.html", **question_data)


# Play random post
@html_bp.route("/play/<int:question_id>", methods=["POST"])
def play_random_submit(question_id):
    # Retrieve user-submited answer
    answer = request.form.get("answer")
    # Retrieve question from database based on id in URL
    question = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    # Create dictionary to be passed to Flask template
    question_data = question.to_dict()
    question_data.update(
        {
            "answers": json.loads(question.incorrect_answers_string)
            + [question.correct_answer],
            "next_question_id": random_question_id,
            "answered": True,
            "correct": False,
        }
    )
    if question.correct_answer == answer:
        # If user-submitted answer is correct
        question_data["correct"] = True
        return render_template("play.html", **question_data)
    else:
        # If user-submitted answer is incorrect
        return render_template("play.html", **question_data)
