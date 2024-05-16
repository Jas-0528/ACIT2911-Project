from unittest.mock import patch, MagicMock
from flask import url_for, session


import pytest
from trivia import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home(client):
    with patch('trivia.routes.html.get_categories') as mock_get_categories:
        mock_get_categories.return_value = []
        response = client.get(url_for('html.home'))
        assert response.status_code == 302


def test_home_submit(client):
    with patch('trivia.routes.html.get_user') as mock_get_user, \
         patch('trivia.routes.html.create_quiz') as mock_create_quiz:
        mock_get_user.return_value = MagicMock(id=1)
        response = client.post(url_for('html.home_submit'), data={'category': 'test_category', 'difficulty': 'test_difficulty', 'length': 'test_length'})
        assert response.status_code == 302


def test_play_random(client):
    with patch('trivia.routes.html.get_question') as mock_get_question:
        mock_get_question.return_value = MagicMock(to_play_dict=MagicMock(return_value={}))
        response = client.get(url_for('html.play_random', question_id=1))
        assert response.status_code == 302


def test_play_random_submit(client):
    with patch('trivia.routes.html.get_question') as mock_get_question:
        mock_get_question.return_value = MagicMock(to_play_dict=MagicMock(return_value={}), correct_answer='test_answer')
        response = client.post(url_for('html.play_random_submit', question_id=1), data={'answer': 'test_answer'})
        assert response.status_code == 302


def test_play_quiz(client):
    with patch('trivia.routes.html.get_user') as mock_get_user, \
         patch('trivia.routes.html.get_quiz') as mock_get_quiz, \
         patch('trivia.routes.html.get_question') as mock_get_question:
        mock_get_user.return_value = MagicMock(id=1, quiz=MagicMock(id=1))
        mock_get_quiz.return_value = MagicMock(questions=[MagicMock(answered=0, question_id=1)])
        mock_get_question.return_value = MagicMock(to_play_dict=MagicMock(return_value={}))
        response = client.get(url_for('html.play_quiz'))
        assert response.status_code == 302


def test_play_quiz_submit(client):
    with patch('trivia.routes.html.get_quiz_question') as mock_get_quiz_question, \
         patch('trivia.routes.html.get_question') as mock_get_question:
        mock_get_quiz_question.return_value = MagicMock(question_id=1)
        mock_get_question.return_value = MagicMock(to_play_dict=MagicMock(return_value={}), correct_answer='test_answer')
        with client.session_transaction() as sess:
            sess['quiz_question_id'] = 1
        response = client.post(url_for('html.play_quiz_submit'), data={'answer': 'test_answer'})
        assert response.status_code == 302

