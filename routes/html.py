import json
from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import functions as func
from db import db
from models import Quiz, QuizQuestion, Question, User

html_bp = Blueprint("html", __name__)


# Helper functions
def get_user(user_id):
    return db.get_or_404(User, user_id, description=f"User {user_id} does not exist")


def get_question(question_id):
    return db.get_or_404(
        Question, question_id, description=f"Question {question_id} does not exist"
    )


def get_quiz(quiz_id):
    return db.get_or_404(Quiz, quiz_id, description=f"Quiz {quiz_id} does not exist")


def get_quiz_question(quiz_question_id):
    return db.get_or_404(
        QuizQuestion,
        quiz_question_id,
        description=f"QuizQuestion {quiz_question_id} does not exist",
    )


def get_categories():
    stmt = db.select(Question.category).distinct()
    result = db.session.execute(stmt)
    categories = [row[0] for row in result]
    return categories


def fetch_questions(category="all", difficulty="all", length=5):
    stmt = db.select(Question)

    if category != "all":
        stmt = stmt.where(Question.category == category)

    if difficulty != "all":
        stmt = stmt.where(Question.difficulty == difficulty)

    stmt = stmt.limit(length)

    questions = db.session.execute(stmt).scalars().all()
    return questions


def create_quiz(user, category, difficulty, length):
    # Return existing quiz if exists
    stmt = db.select(Quiz).where(Quiz.user == user)
    existing_quiz = db.session.execute(stmt).scalar()
    if existing_quiz:
        return existing_quiz

    # Otherwise instantiate new quiz
    quiz = Quiz(user=user)
    db.session.add(quiz)
    db.session.commit()

    questions = fetch_questions(category, difficulty, length)
    for question in questions:
        quiz_question = QuizQuestion(quiz=quiz, question=question)
        db.session.add(quiz_question)

    db.session.commit()
    return


# Homepage
@html_bp.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", categories=get_categories())


# Homepage post (create new quiz)
@html_bp.route("/", methods=["POST"])
@login_required
def home_submit():
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")
    length = request.form.get("length")
    user = get_user(current_user.id)
    create_quiz(user, category, difficulty, length)
    return redirect(url_for("html.play_quiz"))


# Play random page
@html_bp.route("/play/random/<int:question_id>", methods=["GET"])
@login_required
def play_random(question_id):
    # Retrieve question from database based on id in URL
    question = get_question(question_id)

    # Create dictionary to be passed to Flask template
    question_data = question.to_play_dict()
    question_data.update({"answered": False, "correct": False, "mode": "random"})
    return render_template("play.html", **question_data)


# Play random post
@html_bp.route("/play/random/<int:question_id>", methods=["POST"])
@login_required
def play_random_submit(question_id):
    # Retrieve question from database based on id in URL
    question = get_question(question_id)

    # Retrieve user-submited answer
    answer = request.form.get("answer")

    # Create dictionary and pass to Flask template
    question_data = question.to_play_dict()
    question_data.update(
        {
            "answered": True,
            "correct": False if question.correct_answer != answer else True,
            "mode": "random",
        }
    )
    return render_template("play.html", **question_data)


# Play quiz page
@html_bp.route("/play/quiz", methods=["GET"])
@login_required
def play_quiz():
    # Retrieve quiz of currently logged in user
    user = get_user(current_user.id)

    # Redirect if there is no quiz to play
    if user.quiz is None:
        return redirect(url_for("html.home"))

    quiz = get_quiz(user.quiz.id)

    # Play the next unanswered question
    try:
        quiz_question = next(qq for qq in quiz.questions if qq.answered == 0)
        question = get_question(quiz_question.question_id)
    except StopIteration:
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for("html.home"))

    # Store ID QuizQuestion ID in session for POST route
    session["quiz_question_id"] = quiz_question.id

    # Create dictionary and pass to Flask template
    question_data = question.to_play_dict()
    question_data.update({"answered": False, "correct": False, "mode": "challenge"})
    return render_template("play.html", **question_data)


# Play quiz post
@html_bp.route("/play/quiz", methods=["POST"])
@login_required
def play_quiz_submit():
    # Retrieve quiz question and corresponding question using session
    quiz_question = get_quiz_question(session.get("quiz_question_id"))
    question = get_question(quiz_question.question_id)

    # Update quiz question answered attribute
    quiz_question.answered = 1
    db.session.commit()

    # Retrieve user-submited answer
    answer = request.form.get("answer")

    # Create dictionary and pass to Flask template
    question_data = question.to_play_dict()
    question_data.update(
        {
            "answered": True,
            "correct": False if question.correct_answer != answer else True,
            "mode": "challenge",
        }
    )
    return render_template("play.html", **question_data)
