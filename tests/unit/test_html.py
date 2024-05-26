import json, pytest
from unittest.mock import MagicMock, patch
from trivia.models import Question, Quiz, QuizQuestion, User
from trivia.routes.html import (
    get_user,
    get_question,
    get_quiz,
    get_quiz_question,
    get_categories,
    fetch_questions,
    create_quiz,
    update_score,
)


# Session fixture
@pytest.fixture
def mock_session(monkeypatch):
    with patch("trivia.db.db.session") as mock_session:
        yield mock_session


def test_get_user(mock_session):
    # Set up a user with ID 123
    mock_user = User(
        email="user123@example.com", username="user123", password="password123"
    )
    mock_user.id = 123
    mock_session.execute.return_value.scalar.return_value = mock_user

    # Call get_user with ID 123
    user = get_user(123)

    # Assert that get_user returned the correct user
    assert user.id == 123
    assert user.email == "user123@example.com"
    assert user.username == "user123"

    # Assert that get_user called session.execute once
    mock_session.execute.assert_called_once()


def test_get_question(mock_session):
    # Set up a question with ID 456
    mock_question = Question(
        category="Testing",
        difficulty="easy",
        question="What language is this written in?",
        correct_answer="Python",
        incorrect_answers_string=json.dumps(["C", "JavaScript", "Rust"]),
    )
    mock_question.id = 456
    mock_session.execute.return_value.scalar.return_value = mock_question

    # Call get_question with the ID 456
    question = get_question(456)

    # Assert that get_question returned the correct question
    assert question.id == 456
    assert question.category == "Testing"
    assert question.difficulty == "easy"
    assert question.question == "What language is this written in?"
    assert question.correct_answer == "Python"
    assert question.incorrect_answers_string == '["C", "JavaScript", "Rust"]'

    # Assert that get_question called session.execute once
    mock_session.execute.assert_called_once()


def test_get_quiz(mock_session):
    # Set up a quiz with ID 789
    mock_quiz = Quiz(
        user_id=123,
        score=5,
    )
    mock_quiz.id = 789
    mock_session.execute.return_value.scalar.return_value = mock_quiz

    # Call get_quiz with the ID 789
    quiz = get_quiz(789)

    # Assert that get_quiz returned the correct quiz
    assert quiz.id == 789
    assert quiz.user_id == 123
    assert quiz.score == 5

    # Assert that get_quiz called session.execute once
    mock_session.execute.assert_called_once()


def test_get_quiz_question(mock_session):
    # Set up a quiz question with ID 420
    mock_quiz_question = QuizQuestion(quiz_id=789, question_id=456, answered=False)
    mock_quiz_question.id = 420
    mock_session.execute.return_value.scalar.return_value = mock_quiz_question

    # Call get_quiz_question with the ID 420
    quiz_question = get_quiz_question(420)

    # Assert that get_quiz_question returned the correct quiz question
    assert quiz_question.id == 420
    assert quiz_question.quiz_id == 789
    assert quiz_question.question_id == 456
    assert quiz_question.answered == False

    # Assert that get_quiz_question called session.execute once
    mock_session.execute.assert_called_once()


def test_get_categories(mock_session):
    # Set up three categories in the mock database
    mock_categories = ["Entertainment: Video Games", "Geography", "Animals"]
    mock_session.execute.return_value = [(category,) for category in mock_categories]

    categories = get_categories()

    # Assert that get_categories returned the correct categories
    assert categories == sorted(mock_categories)

    # Assert that get_categories called session.execute once
    mock_session.execute.assert_called_once()


def test_fetch_questions(mock_session):
    # Set up three questions in the mock database
    mock_questions = [MagicMock(spec=Question) for _ in range(3)]
    mock_session.execute.return_value.scalars.return_value.all.return_value = (
        mock_questions
    )

    questions = fetch_questions()

    # Assert that fetch_questions returned a three-element object
    assert len(questions) == 3


def test_create_quiz_existing_quiz(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Set up mock_session to return a mock Quiz object when execute().scalar() is called
    mock_session.execute.return_value.scalar.return_value = MagicMock(spec=Quiz)

    # Call create_quiz with the mock User object
    result = create_quiz(
        user=mock_user, category="Geography", difficulty="easy", length=3
    )

    # Assert that create_quiz returned True (because an existing quiz was found)
    assert result is True

    # Assert that create_quiz did not call session.add or .commit
    assert mock_session.add.call_count == 0
    assert mock_session.commit.call_count == 0


def test_create_quiz_no_existing_quiz(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Set up mock_session to return None when execute().scalar() is called
    mock_session.execute.return_value.scalar.return_value = None

    # Mock the fetch_questions function to return a list of 3 mock questions
    with patch(
        "trivia.routes.html.fetch_questions",
        return_value=[
            MagicMock(spec=Question, _sa_instance_state=MagicMock()) for _ in range(3)
        ],
    ):
        # Call create_quiz with the mock User object
        result = create_quiz(
            user=mock_user, category="Geography", difficulty="easy", length=3
        )

    # Assert that create_quiz returned True
    assert result is True

    # Assert that create_quiz called session.add four times and session.commit twice
    assert mock_session.add.call_count == 4
    assert mock_session.commit.call_count == 2


def test_create_quiz_insufficient_questions(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Mock the fetch_questions function to return a list of 2 mock questions
    with patch(
        "trivia.routes.html.fetch_questions",
        return_value=[
            MagicMock(spec=Question, _sa_instance_state=MagicMock()) for _ in range(2)
        ],
    ):
        # Call create_quiz with the mock User object
        result = create_quiz(
            user=mock_user, category="Geography", difficulty="easy", length=3
        )

        # Assert that create_quiz returned False
        assert result is False

        # Assert that create_quiz did not call session.add or session.commit
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_called()


def test_update_score(mock_session):
    # Set up a mock Quiz object
    mock_quiz = MagicMock(spec=Quiz)
    mock_quiz.score = 0

    # Correct answer
    play_data = {"correct_answer": "Brain", "difficulty": "easy"}
    user_answer = "Brain"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 1

    # Correct answer
    play_data = {"correct_answer": "Barbados", "difficulty": "medium"}
    user_answer = "Barbados"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 3

    # Correct answer
    play_data = {"correct_answer": "Hoatzin", "difficulty": "hard"}
    user_answer = "Hoatzin"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 6

    # Incorrect answer
    play_data = {"correct_answer": "Cupertino, California", "difficulty": "hard"}
    user_answer = "Redwood City, California"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 6

    mock_session.commit.call_count == 3
