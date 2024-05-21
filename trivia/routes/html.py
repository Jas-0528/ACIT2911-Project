from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import functions as func
from trivia.db import db
from trivia.models import Quiz, QuizQuestion, Question, User

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


# Get categories (can be used in user category selection)
def get_categories():
    stmt = db.select(Question.category).distinct()
    result = db.session.execute(stmt)
    categories = [row[0] for row in result]
    categories.sort()
    return categories


# Fetch questions based on specified parameters
def fetch_questions(category="all", difficulty="all", length=5):
    stmt = db.select(Question)

    if category != "all":
        stmt = stmt.where(Question.category == category)

    if difficulty != "all":
        stmt = stmt.where(Question.difficulty == difficulty)

    stmt = stmt.order_by(func.random()).limit(length)

    questions = db.session.execute(stmt).scalars().all()
    return questions


# Create Quiz with QuizQuestions
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
    return quiz


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
    play_data = question.to_play_dict()
    play_data.update({"answered": False, "correct": False, "mode": "random"})

    # Store play_data in session
    session["play_data"] = play_data

    return render_template("play.html", **play_data)


# Play random post
@html_bp.route("/play/random/submit", methods=["POST"])
@login_required
def play_random_submit():
    # Retrieve user-submitted answer
    answer = request.form.get("answer")

    # Retrieve play_data from session and update
    play_data = session.get("play_data")
    play_data.update(
        {
            "answered": True,
            "correct": False if play_data["correct_answer"] != answer else True,
            "mode": "random",
        }
    )
    return render_template("play.html", **play_data)


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

    # Create dictionary and pass to Flask template
    play_data = question.to_play_dict()
    play_data.update(
        {
            "answered": False,
            "correct": False,
            "mode": "challenge",
            "score": quiz.score,
        }
    )

    # Store play_data and quiz_question ID in session
    session["play_data"] = play_data
    session["quiz_question_id"] = quiz_question.id

    return render_template("play.html", **play_data)


# Play quiz post
@html_bp.route("/play/quiz/submit", methods=["POST"])
@login_required
def play_quiz_submit():
    # Retrieve quiz question and quiz
    quiz_question = get_quiz_question(session.get("quiz_question_id"))
    quiz = get_quiz(quiz_question.quiz_id)

    # Update answered attribute
    quiz_question.answered = 1
    db.session.commit()

    # Retrieve user-submitted answer
    answer = request.form.get("answer")

    # Retrieve play_data from session and update
    play_data = session.get("play_data")

    # If answer is correct, add to score based on difficulty
    if play_data["correct_answer"] == answer:
        if play_data["difficulty"] == "easy":
            quiz.score += 1
        elif play_data["difficulty"] == "medium":
            quiz.score += 2
        else:
            quiz.score += 3
        db.session.commit()

    # Update data to be passed to template
    play_data.update(
        {
            "answered": True,
            "correct": False if play_data["correct_answer"] != answer else True,
            "mode": "challenge",
            "score": quiz.score,
        }
    )
    return render_template("play.html", **play_data)
