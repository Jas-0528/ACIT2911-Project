from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import functions as func
from trivia.db import db
from trivia.models import Quiz, QuizQuestion, Question, User

html_bp = Blueprint("html", __name__)


# Helper functions
def get_user(user_id):
    stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(stmt).scalar()
    return user


def get_question(question_id):
    stmt = db.select(Question).where(Question.id == question_id)
    question = db.session.execute(stmt).scalar()
    return question


def get_quiz(quiz_id):
    stmt = db.select(Quiz).where(Quiz.id == quiz_id)
    quiz = db.session.execute(stmt).scalar()
    return quiz


def get_quiz_question(quiz_question_id):
    stmt = db.select(QuizQuestion).where(QuizQuestion.id == quiz_question_id)
    quiz_question = db.session.execute(stmt).scalar()
    return quiz_question


# Get categories (can be used in user category selection)
def get_categories():
    stmt = db.select(Question.category).distinct()
    result = db.session.execute(stmt)
    categories = [row[0] for row in result]
    categories.sort()
    return categories


# Fetch questions based on specified parameters, returns them in random order
def fetch_questions(category="all", difficulty="all", length=5):
    stmt = db.select(Question)

    if category != "all":
        stmt = stmt.where(Question.category == category)

    if difficulty != "all":
        stmt = stmt.where(Question.difficulty == difficulty)

    stmt = stmt.order_by(func.random()).limit(length)

    questions = db.session.execute(stmt).scalars().all()
    return questions


# Create Quiz with QuizQuestions if one does not already exist
def create_quiz(user, category, difficulty, length):
    # Return if existing quiz exists
    stmt = db.select(Quiz).where(Quiz.user == user)
    existing_quiz = db.session.execute(stmt).scalar()
    if existing_quiz:
        return

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
    # Retrieve currently logged in user and pass a boolean to the template representing if they have a quiz
    user = get_user(current_user.id)
    return render_template(
        "home.html", categories=get_categories(), quiz_exists=bool(user.quiz)
    )


# Homepage resume Quiz post
@html_bp.route("/resume-quiz", methods=["POST"])
@login_required
def home_submit_resume():
    return redirect(url_for("html.play_quiz"))


# Homepage delete Quiz post
@html_bp.route("/delete-quiz", methods=["POST"])
@login_required
def home_submit_delete():
    # Retrieve currently logged in user
    user = get_user(current_user.id)

    # Retrieve their quiz and delete
    quiz = get_quiz(user.quiz.id)
    db.session.delete(quiz)
    db.session.commit()

    return redirect(url_for("html.home"))


# Homepage play (create) Quiz post
@html_bp.route("/play", methods=["POST"])
@login_required
def home_submit_play():
    user = get_user(current_user.id)
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")
    length = request.form.get("length")
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
    # Retrieve currently logged in user
    user = get_user(current_user.id)

    # Redirect if there is no quiz to play
    if user.quiz is None:
        return redirect(url_for("html.home"))

    # Retrieve their quiz
    quiz = get_quiz(user.quiz.id)

    # Play the next unanswered question
    quiz_question = next((qq for qq in quiz.questions if qq.answered == 0), None)
    if quiz_question is None:
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for("html.home"))

    # Get the question associated with quiz_question
    question = get_question(quiz_question.question_id)

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
    # Retrieve quiz question and redirect home if quiz question doesn't exist
    quiz_question = get_quiz_question(session.get("quiz_question_id"))
    if quiz_question is None:
        return redirect(url_for("html.home"))

    # Retrieve quiz and redirect home if quiz doesn't exist
    quiz = get_quiz(quiz_question.quiz_id)
    if quiz is None:
        return redirect(url_for("html.home"))

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

    # Check if all quiz questions have been answered
    all_answered = all(qq.answered == 1 for qq in quiz.questions)

    # Render the template before deleting the quiz
    response = render_template("play.html", **play_data)

    # Delete quiz if all quiz questions have been answered
    if all_answered:
        db.session.delete(quiz)
        db.session.commit()

    return response
