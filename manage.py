import html, json, random, requests
from sqlalchemy.sql import functions as func
from trivia.db import db
from app import app
from trivia.models import User, Quiz, Question, QuizQuestion


def write_to_json():
    # Make API request to OpenTDB
    url = "https://opentdb.com/api.php?amount=50&type=multiple"
    response = requests.get(url)
    data = response.json()["results"]
    print("Converted to JSON")

    # Write out JSON to file
    with open("data/trivia.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Written to file")


def append_to_json():
    # Make API request to OpenTDB
    url = "https://opentdb.com/api.php?amount=50&type=multiple"
    response = requests.get(url)
    data = response.json()["results"]
    print("Converted to JSON")

    # Read existing data
    try:
        with open("data/trivia.json", "r") as infile:
            existing_data = json.load(infile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    # Append new data
    existing_data.extend(
        question_json for question_json in data if question_json not in existing_data
    )

    # Write out JSON to file
    with open("data/trivia.json", "w") as outfile:
        json.dump(existing_data, outfile, indent=4)
    print("Appended to file")


# Create database tables
def create_all():
    db.create_all()
    print("All tables created")


# Drop database tables
def drop_all():
    db.drop_all()
    print("All tables dropped")


# Add questions to the database from json file created from the API
def add_questions():
    # Read the trivia.json file
    with open("data/trivia.json") as file:
        data = json.load(file)

    # Loop though each question and add it to the database
    for question_json in data:
        question = Question(
            question=html.unescape(question_json["question"]),
            correct_answer=html.unescape(question_json["correct_answer"]),
            incorrect_answers_string=json.dumps(
                [html.unescape(answer) for answer in question_json["incorrect_answers"]]
            ),
            category=html.unescape(question_json["category"]),
            difficulty=html.unescape(question_json["difficulty"]),
        )
        # Add the question to the database
        db.session.add(question)

    # Once all questions have been added, commit the transaction
    db.session.commit()
    print("All questions added")


# Create test user and admin
def create_test_accounts():
    user = User(
        role="user",
        email="user1@example.com",
        username="user1",
        password="password1",
    )
    db.session.add(user)
    admin = User(
        role="admin",
        email="admin1@example.com",
        username="admin1",
        password="password1",
    )
    db.session.add(admin)

    # Once all users have been added, commit
    db.session.commit()
    print("Test user and admin created")


def create_random_game():
    # Find a random user
    user_stmt = db.select(User).order_by(func.random()).limit(1)
    user = db.session.execute(user_stmt).scalar()

    # Make an game
    game = Quiz(user=user)
    db.session.add(game)

    # Sample 1 to 4 questions from the Question table and create a list of database objects
    random_question_stmt = (
        db.select(Question).order_by(func.random()).limit(random.randint(1, 4))
    )
    questions = db.session.execute(random_question_stmt).scalars()

    # Loop over game questions in sample
    for question in questions:

        # Create QuizQuestion objects and add to database
        game_question = QuizQuestion(
            game=game,
            question=question,
        )
        db.session.add(game_question)

    # Commit to database
    db.session.commit()
    print("Random game created")


if __name__ == "__main__":
    with app.app_context():
        # write_to_json()
        # append_to_json()
        drop_all()
        create_all()
        add_questions()
        create_test_accounts()
        # create_random_game()
