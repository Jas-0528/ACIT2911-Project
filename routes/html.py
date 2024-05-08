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
    question_obj = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("play.html", question=question_obj.to_game_dict(), random_id=random_id)


# Game page post
@html_bp.route("/play/<int:question_id>/submit", methods=["POST"])
def play_question_submit(question_id):
    answer = request.form.get("answer")
    question_obj = db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )
    if question_obj.correct_answer == answer:
        return "true"
    else:
        return "false"
