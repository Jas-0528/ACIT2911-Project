from unittest.mock import MagicMock, patch
from trivia.models import Question, Quiz, User
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


def test_get_user(user, mock_session):
    # Set up a user with ID 123
    user.id = 123
    mock_session.execute.return_value.scalar.return_value = user

    # Call get_user with ID 123
    retrieved_user = get_user(123)

    # Assert that get_user returned the correct user
    assert retrieved_user.id == 123
    assert retrieved_user.email == "user9@example.com"
    assert retrieved_user.username == "user9"

    # Assert that get_user called session.execute once
    mock_session.execute.assert_called_once()


def test_get_question(question, mock_session):
    # Set up a question with ID 456
    question.id = 456
    mock_session.execute.return_value.scalar.return_value = question

    # Call get_question with the ID 456
    retrieved_question = get_question(456)

    # Assert that get_question returned the correct question
    assert retrieved_question.id == 456
    assert retrieved_question.category == "Geography"
    assert retrieved_question.difficulty == "Hard"
    assert retrieved_question.question == "Which is not a country in Africa?"
    assert retrieved_question.correct_answer == "Guyana"
    assert (
        retrieved_question.incorrect_answers_string
        == '["Senegal", "Liberia", "Somalia"]'
    )

    # Assert that get_question called session.execute once
    mock_session.execute.assert_called_once()


def test_get_quiz(quiz, mock_session):
    # Set up a quiz with ID 789
    quiz.id = 789
    quiz.user_id = 123
    quiz.score = 5
    mock_session.execute.return_value.scalar.return_value = quiz

    # Call get_quiz with the ID 789
    retrieved_quiz = get_quiz(789)

    # Assert that get_quiz returned the correct quiz
    assert retrieved_quiz.id == 789
    assert retrieved_quiz.user_id == 123
    assert retrieved_quiz.score == 5

    # Assert that get_quiz called session.execute once
    mock_session.execute.assert_called_once()


def test_get_quiz_question(quiz_question, mock_session):
    # Set up a quiz question with ID 420
    quiz_question.id = 420
    quiz_question.quiz_id = 789
    quiz_question.question_id = 456
    quiz_question.answered = False
    mock_session.execute.return_value.scalar.return_value = quiz_question

    # Call get_quiz_question with the ID 420
    retrieved_quiz_question = get_quiz_question(420)

    # Assert that get_quiz_question returned the correct quiz question
    assert retrieved_quiz_question.id == 420
    assert retrieved_quiz_question.quiz_id == 789
    assert retrieved_quiz_question.question_id == 456
    assert retrieved_quiz_question.answered == False

    # Assert that get_quiz_question called session.execute once
    mock_session.execute.assert_called_once()


def test_get_categories(mock_session):
    # Set up three categories in the mock database
    mock_categories = ["Entertainment: Video Games", "Geography", "Animals"]
    mock_session.execute.return_value = [(category,) for category in mock_categories]

    retrieved_categories = get_categories()

    # Assert that get_categories returned the correct categories
    assert retrieved_categories == sorted(mock_categories)

    # Assert that get_categories called session.execute once
    mock_session.execute.assert_called_once()


def test_fetch_questions(mock_session):
    # Set up three questions in the mock database
    mock_questions = [MagicMock(spec=Question) for _ in range(3)]
    mock_session.execute.return_value.scalars.return_value.all.return_value = (
        mock_questions
    )

    fetched_questions = fetch_questions()

    # Assert that fetch_questions returned a three-element object
    assert len(fetched_questions) == 3


def test_create_quiz_existing_quiz(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Set up mock_session to return a mock Quiz object (an existing quiz was found)
    mock_session.execute.return_value.scalar.return_value = MagicMock(spec=Quiz)

    # Call create_quiz with the mock User object
    result = create_quiz(
        user=mock_user, category="Geography", difficulty="Easy", length=3
    )

    # Assert that create_quiz returned True (an existing quiz can be played)
    assert result is True

    # Assert that create_quiz did not call session.add or .commit
    assert mock_session.add.call_count == 0
    assert mock_session.commit.call_count == 0


def test_create_quiz_no_existing_quiz(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Set up mock_session to return None (no existing quiz was found)
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
            user=mock_user, category="Geography", difficulty="Easy", length=3
        )

    # Assert that create_quiz returned True (an newly created quiz can be played)
    assert result is True

    # Assert that create_quiz called session.add four times and session.commit twice
    assert mock_session.add.call_count == 4
    assert mock_session.commit.call_count == 2


def test_create_quiz_insufficient_questions(mock_session):
    # Set up a mock User object
    mock_user = MagicMock(spec=User)
    mock_user.id = 123
    mock_user._sa_instance_state = MagicMock()

    # Set up mock_session to return None (no existing quiz was found)
    mock_session.execute.return_value.scalar.return_value = None

    # Mock the fetch_questions function to return a list of 2 mock questions
    with patch(
        "trivia.routes.html.fetch_questions",
        return_value=[
            MagicMock(spec=Question, _sa_instance_state=MagicMock()) for _ in range(2)
        ],
    ):
        # Call create_quiz with the mock User object
        result = create_quiz(
            user=mock_user, category="Geography", difficulty="Easy", length=3
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
    play_data = {"correct_answer": "Brain", "difficulty": "Easy"}
    user_answer = "Brain"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 1

    # Correct answer
    play_data = {"correct_answer": "Barbados", "difficulty": "Medium"}
    user_answer = "Barbados"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 3

    # Correct answer
    play_data = {"correct_answer": "Hoatzin", "difficulty": "Hard"}
    user_answer = "Hoatzin"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 6

    # Incorrect answer
    play_data = {"correct_answer": "Cupertino, California", "difficulty": "Hard"}
    user_answer = "Redwood City, California"
    update_score(mock_quiz, play_data, user_answer)
    assert mock_quiz.score == 6

    mock_session.commit.call_count == 3
