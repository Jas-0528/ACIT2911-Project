import os, pytest
from flask import url_for
from app import app
from trivia.db import db
from trivia.models import User
from trivia.routes import auth


# Client fixture with SERVER_NAME and PORT
@pytest.fixture
def client():
    port = os.getenv("PORT", "8888")
    app.config["SERVER_NAME"] = f"localhost:{port}"
    with app.app_context():
        with app.test_client() as client:
            yield client


# Create user for testing
@pytest.fixture
def setup_user():
    with app.app_context():
        user = auth.User.query.filter_by(username="test").first()
        if user:
            auth.db.session.delete(user)
            auth.db.session.commit()
        user = auth.User(
            username="test", email="testing@gmail.com", password="password"
        )
        auth.db.session.add(user)
        auth.db.session.commit()
        yield user
        auth.db.session.delete(user)
        auth.db.session.commit()


# Test if user is in the database
def test_user_in_db(setup_user):
    stmt = db.select(User).where(User.username == "test")
    result = db.session.execute(stmt)
    user = result.scalars().first()
    assert user is not None
    assert user.username == "test"


# Test auth.login function -> check if the login page is rendered
def test_login_page(client):
    response = client.get(url_for("auth.login"))
    assert response.status_code == 200


# Test auth.register function -> check if the register page is rendered
def test_register_page(client):
    response = client.get(url_for("auth.register"))
    assert response.status_code == 200
