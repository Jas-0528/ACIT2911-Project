import pytest
from unittest.mock import MagicMock, patch
from trivia.db import db
from trivia.models import Question, User, Quiz, QuizQuestion
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


@pytest.fixture
def mock_session():
    with patch('trivia.db.db.session') as mock_session:
        mock_session.commit = MagicMock()
        mock_session.add = MagicMock()
        yield mock_session


class MockDB:
    def get_or_404(self, model, id, description):
        pass

@pytest.fixture
def mock_db(monkeypatch):
    mock_db_instance = MagicMock()
    monkeypatch.setattr('trivia.db', mock_db_instance)
    return mock_db_instance

db = MockDB()

def test_retrieval_functions():
    with pytest.raises(Exception):  
        get_user(123)  
    with pytest.raises(Exception):  
        get_question(456) 
""""
def test_get_categories(mock_db):
    expected_categories = ['category1', 'category2']
    mock_db.select.return_value = MagicMock(
        execute = MagicMock(return_value=MagicMock(
            scalars = MagicMock(return_value=expected_categories)
        ))
    )
    assert get_categories() == expected_categories
    mock_db.select.assert_called_once()
    mock_db.select().distinct.assert_called_once_with(Question.category) 
"""

def test_get_quiz(mock_session):
    mock_quiz = MagicMock(spec=Quiz)
    mock_session.execute.return_value.scalar.return_value = mock_quiz
    
    quiz = get_quiz(1)
    
    mock_session.execute.assert_called_once()
    assert quiz == mock_quiz

def test_get_quiz_question(mock_session):
    mock_quiz_question = MagicMock(spec=QuizQuestion)
    mock_session.execute.return_value.scalar.return_value = mock_quiz_question
    
    quiz_question = get_quiz_question(1)
    
    mock_session.execute.assert_called_once()
    assert quiz_question == mock_quiz_question

def test_get_categories(mock_session):
    mock_session.execute.return_value = [('category1',), ('category2',)]
    
    categories = get_categories()
    
    mock_session.execute.assert_called_once()
    assert categories == ['category1', 'category2']

def test_fetch_questions(mock_session):
    mock_questions = [MagicMock(spec=Question) for _ in range(5)]
    mock_session.execute.return_value.scalars.return_value.all.return_value = mock_questions
    
    questions = fetch_questions(length=5)
    
    mock_session.execute.assert_called_once()
    assert questions == mock_questions

def test_create_quiz(mock_session):
    mock_user = MagicMock(spec=User)
    mock_user._sa_instance_state = MagicMock()  # add this line
    print(mock_user._sa_instance_state)  # add this line
    mock_quiz = MagicMock(spec=Quiz)
    mock_session.add.side_effect = None
    mock_session.commit.return_value = None

    # Create the mock_question object
    mock_question = MagicMock(spec=Question)
    mock_question._sa_instance_state = MagicMock()

    with patch('trivia.routes.html.fetch_questions', return_value=[mock_question for _ in range(5)]):
        result = create_quiz(mock_user, 'category', 'difficulty', 5)

def test_create_quiz_insufficient_questions(mock_session):
    mock_user = MagicMock(spec=User)
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    
    with patch('trivia.routes.html.fetch_questions', return_value=[MagicMock(spec=Question) for _ in range(3)]):
        result = create_quiz(mock_user, 'category', 'difficulty', 5)
    
    assert result is False

def test_update_score(mock_session):

    mock_quiz = MagicMock(spec=Quiz)
    mock_quiz.score = 0


    play_data = {'correct_answer': 'A', 'difficulty': 'easy'}
    user_answer = 'A'  # Correct answer

 
    update_score(mock_quiz, play_data, user_answer)

    assert mock_quiz.score == 1  
    play_data = {'correct_answer': 'A', 'difficulty': 'medium'}
    user_answer = 'A'  
    update_score(mock_quiz, play_data, user_answer)

    assert mock_quiz.score == 3  
    play_data = {'correct_answer': 'A', 'difficulty': 'hard'}
    user_answer = 'A'  
    update_score(mock_quiz, play_data, user_answer)

    assert mock_quiz.score == 6  
    play_data = {'correct_answer': 'A', 'difficulty': 'hard'}
    user_answer = 'B'  # Incorrect answer

    update_score(mock_quiz, play_data, user_answer)
    
    assert mock_quiz.score == 6  
    mock_session.commit.assert_called()

def test_update_score_incorrect_answer(mock_session):
    mock_quiz = MagicMock(spec=Quiz)
    mock_quiz.score = 0  # Set score to 0
    play_data = {'correct_answer': 'A', 'difficulty': 'medium'}

    update_score(mock_quiz, play_data, 'B')

    assert mock_quiz.score == 0
    mock_session.commit.assert_not_called()





