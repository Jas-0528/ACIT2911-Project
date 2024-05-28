import os, pytest
from flask import url_for
from app import app


def test_question_list(client):
    response = client.get(url_for("api.question_list"))

    assert response.status_code == 200
    assert response.is_json

    # Get the JSON data from the response
    data = response.get_json()

    # Check that the data is a list
    assert isinstance(data, list)

    # Check the structure of each item in the list
    for question_json in data:
        assert "id" in question_json
        assert "category" in question_json
        assert "difficulty" in question_json
        assert "question" in question_json
        assert "correct_answer" in question_json
        assert "incorrect_answers" in question_json

        # Check that incorrect_answers is a list
        assert isinstance(question_json["incorrect_answers"], list)
