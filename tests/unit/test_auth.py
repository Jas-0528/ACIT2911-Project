import pytest
from trivia.routes import auth
from trivia import app




# Create user for testing
@pytest.fixture
def create_user():
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

#test if user is in the database
def test_user_in_db(create_user):
    with app.app_context():
        user = auth.User.query.filter_by(email="testing@gmail.com").first()
        assert user is not None
        assert user.username == "test"

# Test auth.login function -> check if the login page is rendered
def test_login_page():
    with app.test_client() as client:
        response = client.get("auth/login")
        assert response.status_code == 200

#test if current user is authenticated
def test_current_user_authenticated(create_user):
    with app.app_context():
        user = auth.User.query.filter_by(email="testing@gmail.com").first()
        assert user.is_authenticated == False

# Test login post -> check if the user is logged in successfully
def test_login_post(create_user):
    #test successful login with correct email and password
    with app.test_client() as client:
        response = client.post(
            "auth/login",
            data=dict(email=create_user.email, password="password"),
            follow_redirects=True,
        )
        assert response.status_code == 200


# Test auth.register function -> check if the register page is rendered
def test_register_page():
    with app.test_client() as client:
        response = client.get("auth/register")
        assert response.status_code == 200




# Test register post -> check if the user is registered successfully
def test_register_post_invalid(create_user):
    with app.test_client() as client:
        # Test with existing user email
        response = client.post(
            "auth/register",
            data=dict(email=create_user.email, password="password", name="test"),
            follow_redirects=True,
        )
        assert response.status_code == 200


        # Test with existing user username
        response = client.post(
            "auth/register",
            data=dict(
                email="tests123@gmail.con",
                password="password",
                name=create_user.username,
            ),
            follow_redirects=True,
        )
        assert response.status_code == 200




def test_register_post_invalid_email(create_user):
    with app.test_client() as client:
        # Test with invalid email
        response = client.post(
            "auth/register",
            data=dict(email="invalid", password="password", name="test"),
            follow_redirects=True,
        )
        assert response.status_code == 200




def test_register_post_valid():
    with app.test_client() as client:
        # Test with new user email and username and dont save in database
        response = client.post(
            "auth/register",
            data=dict(email="test2@gmail.com", password="password", name="test2"),
            follow_redirects=True,
        )
        assert response.status_code == 200

#delete the registered user
def test_delete_user():
    with app.app_context():
        user = auth.User.query.filter_by(email="test2@gmail.com").first()
        auth.db.session.delete(user)
        auth.db.session.commit()

# Test logout function
def test_logout():
    with app.test_client() as client:
        response = client.get("auth/logout")
        assert response.status_code == 302


