from flask import (
    after_this_request,
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
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


# Create Quiz and fill with QuizQuestions
def create_quiz(user, category, difficulty, length):
    # Check for existing quiz skip creation if true
    stmt = db.select(Quiz).where(Quiz.user_id == user.id)
    existing_quiz = db.session.execute(stmt).scalar()
    if existing_quiz:
        return True

    # Fetch questions
    questions = fetch_questions(category, difficulty, length)

    # Abort if the number of the questions is less than requested
    if len(questions) < length:
        return False

    # Otherwise instantiate new quiz
    quiz = Quiz(user=user)
    db.session.add(quiz)
    db.session.commit()

    for question in questions:
        quiz_question = QuizQuestion(quiz=quiz, question=question)
        db.session.add(quiz_question)

    db.session.commit()
    return True


# If answer is correct, update score based on difficulty
def update_score(quiz, play_data, answer):
    if play_data["correct_answer"] == answer:
        if play_data["difficulty"] == "easy":
            quiz.score += 1
        elif play_data["difficulty"] == "medium":
            quiz.score += 2
        else:
            quiz.score += 3
        db.session.commit()


# Routes
# Homepage
@html_bp.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return render_template("home.html", categories=get_categories())
    else:
        return redirect(url_for("auth.login"))


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

    # Get quiz mode parameters
    category = request.form.get("category")
    difficulty = request.form.get("difficulty")
    length = int(request.form.get("length"))

    # Ensure a quiz exists
    created = create_quiz(user, category, difficulty, length)
    if not created:
        flash(
            "Not enough questions to create a quiz. Please try again with a different category or difficulty."
        )
        return redirect(url_for("html.home"))
    return redirect(url_for("html.play_quiz"))


# Play random page
@html_bp.route("/play/random/<int:question_id>", methods=["GET"])
@login_required
def play_random(question_id):
    # Prevent page caching
    @after_this_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store"
        return response

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
        }
    )
    return render_template("play.html", **play_data)


# Play quiz page
@html_bp.route("/play/quiz", methods=["GET"])
@login_required
def play_quiz():
    # Prevent page caching
    @after_this_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store"
        return response

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
            "mode": "quiz",
            "score": quiz.score,
            "questions_done": quiz_question.id,
            "questions_total": len(quiz.questions),
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

    # Retrieve user-submitted answer and play_data from session
    answer = request.form.get("answer")
    play_data = session.get("play_data")

    # Update score
    if quiz_question.answered == 0:
        update_score(quiz, play_data, answer)

    # Update answered attribute
    quiz_question.answered = 1
    db.session.commit()

    # Update data to be passed to template and render the template
    play_data.update(
        {
            "answered": True,
            "correct": False if play_data["correct_answer"] != answer else True,
            "score": quiz.score,
        }
    )
    response = render_template("play.html", **play_data)

    # Delete quiz if all quiz questions have been answered
    if all(qq.answered == 1 for qq in quiz.questions):
        db.session.delete(quiz)
        db.session.commit()

    return response
