import os, pytest
from flask import url_for
from flask_login import current_user
from app import app
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
            username="test", email="testing@gmail.com", password="Pa55word"
        )
        auth.db.session.add(user)
        auth.db.session.commit()
        yield user
        auth.db.session.delete(user)
        auth.db.session.commit()


# Test login post -> check if the user is logged in successfully with email
def test_login_email(client, setup_user):
    # Test successful login with correct email and password
    response = client.post(
        url_for("auth.login"),
        data=dict(login_method=setup_user.email, password="Pa55word"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.location == url_for("html.home")
    assert current_user.is_authenticated


# Test login post -> check if the user is logged in successfully with username
def test_login_username(client, setup_user):
    # Test successful login with correct username and password
    response = client.post(
        url_for("auth.login"),
        data=dict(login_method=setup_user.username, password="Pa55word"),
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert response.location == url_for("html.home")
    assert current_user.is_authenticated


# Test login post -> check if the user is not logged in with an incorrect password
def test_login_wrong_password(client, setup_user):
    # Test unsuccessful login with incorrect password
    response = client.post(
        url_for("auth.login"),
        data=dict(login_method=setup_user.email, password="wr0ngPa55word"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Incorrect password, try again" in response.data
    assert not current_user.is_authenticated


# Test register post -> check if the user is not registered with existing email
def test_register_existing_email(client, setup_user):
    # Test with existing user email
    response = client.post(
        url_for("auth.register"),
        data=dict(email=setup_user.email, password="Pa55word", username="test"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Email address already in use" in response.data


# Test register post -> check if the user is not registered with existing username
def test_register_existing_username(client, setup_user):
    # Test with existing user username
    response = client.post(
        url_for("auth.register"),
        data=dict(
            email="tests123@gmail.com",
            password="Pa55word",
            username=setup_user.username,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Username already exists" in response.data


# Test register post -> check if the password is too weak
def test_register_weak_password(client):
    # Test with weak password
    response = client.post(
        url_for("auth.register"),
        data=dict(
            email="user420@gmail.com",
            password="password",
            username="user420",
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert (
        b"Password must contain at least one uppercase letter, one lowercase letter, one number, and be at least 8 characters long"
        in response.data
    )


# Test register post -> check all fields are filled
def test_register_empty_fields(client):
    # Test with empty email field
    response = client.post(
        url_for("auth.register"),
        data=dict(
            email="",
            password="password",
            username="user69",
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"All fields are required" in response.data


# Test register post -> check if the user is registered with valid parameters
def test_register_post_valid(client):
    # Test with new user email, username, and password, and don't save in database
    response = client.post(
        url_for("auth.register"),
        data=dict(email="test2@gmail.com", username="test2", password="Pa55word"),
        follow_redirects=True,
    )
    assert response.status_code == 200
    user = auth.User.query.filter_by(email="test2@gmail.com").first()
    assert user is not None
    assert user.email == "test2@gmail.com"
    assert user.username == "test2"
    auth.db.session.delete(user)
    auth.db.session.commit()


# Test logout function
def test_logout(client):
    response = client.get(url_for("auth.logout"))
    assert response.status_code == 302
    assert not current_user.is_authenticated
