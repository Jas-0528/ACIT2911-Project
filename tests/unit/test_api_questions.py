import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from trivia import app as flask_app
from trivia.models import Question
from trivia.db import db

@pytest.fixture
def app():
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_api_question_list(client):
    with patch.object(db.session, 'execute') as mock_execute:
        mock_question = MagicMock()
        mock_question.to_api_dict.return_value = {'id': 1, 'question': 'test_question'}
        mock_execute.return_value.scalars.return_value = [mock_question]

        response = client.get('/api/questions/')
        assert response.status_code == 200
        assert response.get_json() == [{'id': 1, 'question': 'test_question'}]