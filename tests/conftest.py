import os, pytest, uuid
from unittest.mock import patch
from app import app
from trivia.db import db
from trivia.models import Question, Quiz, QuizQuestion, User


@pytest.fixture(autouse=True)
def enable_testing_mode():
    app.config["TESTING"] = True


# Client fixture with SERVER_NAME and PORT
@pytest.fixture
def client():
    port = os.getenv("PORT", "8888")
    app.config["SERVER_NAME"] = f"localhost:{port}"
    with app.app_context():
        with app.test_client() as client:
            yield client


# Session fixture
@pytest.fixture
def mock_session():
    with patch("trivia.db.db.session") as mock_session:
        yield mock_session
        mock_session.reset_mock()


# Basic User fixture
@pytest.fixture
def user():
    user = User(username="user9", email="user9@example.com", password="P@ssw0rd!")
    return user


# Basic Quiz fixture
@pytest.fixture
def quiz(user):
    quiz = Quiz(user=user)
    return quiz


# Basic Question fixture
@pytest.fixture
def question():
    question = Question(
        category="Geography",
        difficulty="hard",
        question="Which is not a country in Africa?",
        correct_answer="Guyana",
        incorrect_answers_string='["Senegal", "Liberia", "Somalia"]',
    )
    return question


# Basic QuizQuestion fixture
@pytest.fixture
def quiz_question(question, quiz):
    quiz_question = QuizQuestion(question=question, quiz=quiz)
    return quiz_question


# User fixture committed to test database
@pytest.fixture
def db_user():
    with app.app_context():
        unique_id = uuid.uuid4()
        user = User(
            username=f"testuser_{unique_id}",
            email=f"testuser_{unique_id}@testing.com",
            password="P@ssw0rd!",
        )
        db.session.add(user)
        db.session.commit()
        yield user
        db.session.delete(user)
        db.session.commit()
