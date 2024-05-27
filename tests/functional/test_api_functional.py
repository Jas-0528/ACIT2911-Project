import os, pytest
from flask import url_for
from app import app


# Client fixture with SERVER_NAME and PORT
@pytest.fixture
def client():
    port = os.getenv("PORT", "8888")
    app.config["SERVER_NAME"] = f"localhost:{port}"
    with app.app_context():
        with app.test_client() as client:
            yield client


def test_question_list(client):
    response = client.get(url_for("api.question_list"))

    assert response.status_code == 200
    assert response.is_json

    # Get the JSON data from the response
    data = response.get_json()

    # Check that the data is a list
    assert isinstance(data, list)

    # Check the structure of each item in the list
    for item in data:
        assert "id" in item
        assert "category" in item
        assert "difficulty" in item
        assert "question" in item
        assert "correct_answer" in item
        assert "incorrect_answers" in item

        # Check that incorrect_answers is a list
        assert isinstance(item["incorrect_answers"], list)
