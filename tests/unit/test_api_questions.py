import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from trivia import app as flask_app
from trivia.models import Question
from trivia.db import db

# Define a fixture for the Flask application
@pytest.fixture
def app():
    # Set the TESTING configuration option to True
    flask_app.config.update({
        'TESTING': True,
    })
    yield flask_app

# Define a fixture for a test client
@pytest.fixture
def client(app):
    return app.test_client()

# Test the api questions endpoint when there's onlk one question in the database
def test_api_question_list(client):
    
    with patch.object(db.session, 'execute') as mock_execute:
      
        mock_question = MagicMock()
       # returns dict
        mock_question.to_api_dict.return_value = {'id': 1, 'question': 'test_question'}
        # Set the return value of the execute method
        mock_execute.return_value.scalars.return_value = [mock_question]

        
        response = client.get('/api/questions/')
        # Check that the status code is 200
        assert response.status_code == 200
        # Check that the JSON response matches the expected output
        assert response.get_json() == [{'id': 1, 'question': 'test_question'}]

# Test the /api/questions/ endpoint when there are no questions in the database
def test_api_question_list_empty(client):
    # Mock the db.session.execute method
    with patch.object(db.session, 'execute') as mock_execute:
        # Set the return value of the execute method to an empty list
        mock_execute.return_value.scalars.return_value = []

        # Send a GET request to the /api/questions/ endpoint
        response = client.get('/api/questions/')
        # Check that the status code is 200
        assert response.status_code == 200
        # Check that the JSON response is an empty list
        assert response.get_json() == []