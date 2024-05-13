import json
from flask import Blueprint, redirect, render_template, request, session, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql import functions as func
from db import db
from models import Game, GameQuestion, Question, User

html_bp = Blueprint("html", __name__)


# Homepage
@html_bp.route("/", methods=["GET"])
@login_required
def home():
    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    return render_template("home.html", next_question_id=random_question_id)


# Homepage post (create new game)
@html_bp.route("/", methods=["POST"])
@login_required
def home_submit():
    # category = request.form.get("category")
    category = "Geography"
    difficulty = "hard"
    # number_of_questions = request.form.get("number_of_questions")
    number_of_questions = 5

    # Retrieve logged in user
    user = db.get_or_404(
        User,
        current_user.id,
        description=f"Question {current_user.id} does not exist",
    )

    # Need to check that user does not already have a game
    # Make a game
    game = Game(user=user)
    db.session.add(game)

    # Commit to database
    db.session.commit()

    stmt = (
        db.select(Question)
        .where(Question.category == category, Question.difficulty == difficulty)
        .limit(number_of_questions)
    )
    questions = db.session.execute(stmt).scalars().all()
    # stmt = db.select(Question).where(Question.category == category).limit(1)
    # question = db.session.execute(stmt).scalar()
    print(questions)


    for question in questions:
        # Create GameQuestion objects and add to database
        game_question = GameQuestion(
            game=game,
            question=question,
        )
        db.session.add(game_question)

    # Commit to database
    db.session.commit()

    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    return render_template("home.html", next_question_id=random_question_id)


# Play random page
@html_bp.route("/play/random/<int:question_id>", methods=["GET"])
@login_required
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
            "play": "random",
        }
    )
    return render_template("play.html", **question_data)


# Play random post
@html_bp.route("/play/random/<int:question_id>", methods=["POST"])
@login_required
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
            "play": "random",
        }
    )
    if question.correct_answer == answer:
        # If user-submitted answer is correct
        question_data["correct"] = True
        return render_template("play.html", **question_data)
    else:
        # If user-submitted answer is incorrect
        return render_template("play.html", **question_data)


# Play game page
@html_bp.route("/play/game", methods=["GET"])
@login_required
def play_game():
    # Retrieve game of currently logged in user
    print(current_user.id)
    game = Game.query.filter(Game.user_id == current_user.id).first()

    if all(game_question.answered for game_question in game.questions):
        random_question_id = (
            db.session.query(Question.id).order_by(func.random()).first()[0]
        )
        db.session.delete(game)
        db.session.commit()
        return render_template("home.html", next_question_id=random_question_id)

    random_question_id = (
        db.session.query(Question.id).order_by(func.random()).first()[0]
    )
    for game_question in game.questions:
        if game_question.answered == 0:
            question = db.get_or_404(
                Question,
                game_question.question_id,
                description=f"Question {game_question.question_id} does not exist",
            )
            break
    session["game_question_id"] = game_question.id
    # Create dictionary to be passed to Flask template
    question_data = question.to_dict()
    question_data.update(
        {
            "answers": json.loads(question.incorrect_answers_string)
            + [question.correct_answer],
            "next_question_id": random_question_id,
            "answered": False,
            "correct": False,
            "play": "game",
        }
    )
    return render_template("play.html", **question_data)


# Play game post
@html_bp.route("/play/game", methods=["POST"])
@login_required
def play_game_submit():
    game_question_id = session.get("game_question_id")
    print(game_question_id)
    # Retrieve user-submited answer
    answer = request.form.get("answer")

    # Retrieve game question based on id session
    game_question = db.get_or_404(
        GameQuestion,
        game_question_id,
        description=f"GameQuestion {game_question_id} does not exist",
    )

    # Retrieve question from database based on id
    question = db.get_or_404(
        Question,
        game_question.question_id,
        description=f"Question {game_question.question_id} does not exist",
    )

    # Update game question answered attribute
    game_question.answered = 1
    db.session.commit()

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
            "play": "game",
        }
    )
    if question.correct_answer == answer:
        # If user-submitted answer is correct
        question_data["correct"] = True
        return render_template("play.html", **question_data)
    else:
        # If user-submitted answer is incorrect
        return render_template("play.html", **question_data)
