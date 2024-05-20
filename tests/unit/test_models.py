import json
import pytest
from werkzeug.security import check_password_hash
from trivia.models import Question, Quiz, QuizQuestion, User


@pytest.fixture
def user():
    # Basic User fixture
    user = User(username="user9", email="user9@example.com", password="password9")
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
    assert user.username == "user9"
    assert user.email == "user9@example.com"
    assert user.password_hashed != "password9"
    assert user.password_hashed is not None


def test_password_hashing(user):
    # Test password hashing
    assert check_password_hash(user.password_hashed, "password9")


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
    play_dict = question.to_play_dict()
    assert play_dict["id"] == question.id
    assert play_dict["category"] == question.category
    assert play_dict["difficulty"] == question.difficulty
    assert play_dict["question"] == question.question
    assert play_dict["correct_answer"] == question.correct_answer
    assert set(play_dict["answers"]) == set(
        json.loads(question.incorrect_answers_string) + [question.correct_answer]
    )
