import json
import pytest
from werkzeug.security import check_password_hash
from trivia.models import Question, Quiz, QuizQuestion, User


@pytest.fixture
def user():
    # Basic User fixture
    user = User(username="drai_29", email="dleon@oilers.ca", password="gooilersgo")
    return user


@pytest.fixture
def quiz(user):
    # Basic Quiz fixture
    quiz = Quiz(user=user)
    return quiz


@pytest.fixture
def question():
    # Basic Question fixture
    question = Question(
        category="Geography",
        difficulty="hard",
        question="Which is not a country in Africa?",
        correct_answer="Guyana",
        incorrect_answers_string=json.dumps(["Senegal", "Liberia", "Somalia"]),
    )
    return question


@pytest.fixture
def quiz_question(question, quiz):
    # Basic QuizQuestion fixture
    quiz_question = QuizQuestion(question=question, quiz=quiz)
    return quiz_question


def test_new_user(user):
    # Test User attributes
    assert user.role == "user"
    assert user.username == "drai_29"
    assert user.email == "dleon@oilers.ca"
    assert user.password_hashed != "gooilersgo"
    assert user.password_hashed is not None


def test_password_hashing(user):
    # Test password hashing
    assert check_password_hash(user.password_hashed, "gooilersgo")


def test_quiz_user_relationship(user, quiz):
    # Test relationship between User and Quiz
    assert quiz.user == user
    assert user.quiz == quiz


def test_question_to_api_dict(question):
    # Test conversion of dictionary for api
    assert question.to_api_dict() == {
        "id": question.id,
        "category": question.category,
        "difficulty": question.difficulty,
        "question": question.question,
        "correct_answer": question.correct_answer,
        "incorrect_answers": json.loads(question.incorrect_answers_string),
    }


def test_question_to_play_dict(question):
    # Test conversion of dictionary for game
    assert question.to_play_dict() == {
        "id": question.id,
        "category": question.category,
        "difficulty": question.difficulty,
        "question": question.question,
        "correct_answer": question.correct_answer,
        "answers": json.loads(question.incorrect_answers_string)
        + [question.correct_answer],
    }
