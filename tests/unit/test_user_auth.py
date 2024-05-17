import pytest
from trivia.routes import auth
from trivia import app

#create user for testing
@pytest.fixture
def create_user():
    with app.app_context():
        user = auth.User(username="test", email="testing@gmail.com", password="password")
        return user

#test auth.login function -> check if the login page is rendered
def test_login_page():
    with app.test_client() as client:
        response = client.get('auth/login')
        assert response.status_code == 200

#test login post -> check if the user is logged in successfully
def test_login_post(create_user):
    with app.test_client() as client:
        #test with existing user email and password
        response = client.post('auth/login', data=dict(email=create_user.email, password="password"))
        assert response.status_code == 302

        #test with existing user username and password
        response = client.post('auth/login', data=dict(email=create_user.username, password="password"))
        assert response.status_code == 302

        #test with non-existing user email and password
        response = client.post('auth/login', data=dict(email="invalid@gmail.con", password="password"),follow_redirects=True)
        assert response.status_code == 200
        assert b"User not found: check login details" in response.data

        #test with non-existing user username and password
        response = client.post('auth/login', data=dict(email="invalid", password="password"),follow_redirects=True)
        assert response.status_code == 200
        assert b"User not found: check login details" in response.data

        #test with  wrong password
        response = client.post('auth/login', data=dict(email=create_user.email, password="wrong"),follow_redirects=True)
        assert response.status_code == 200
        assert b"User not found: check login details" in response.data

        #test with wrong email
        response = client.post('auth/login', data=dict(email="incorrect", password="password"),follow_redirects=True)
        assert response.status_code == 200
        assert b"User not found: check login details" in response.data

        #test with wrrong username
        response = client.post('auth/login', data=dict(username="incorrect", password="password"),follow_redirects=True)
        assert response.status_code == 200

        #log in with remember me
        response = client.post('auth/login', data=dict(email=create_user.email, password="password", remember="on"))
        assert response.status_code == 302

#test auth.register function -> check if the register page is rendered
def test_register_page():
    with app.test_client() as client:
        response = client.get('auth/register')
        assert response.status_code == 200

#test register post -> check if the user is registered successfully
def test_register_post_invalid(create_user):
    with app.test_client() as client:
        #test with existing user email
        response = client.post('auth/register', data=dict(email=create_user.email, password="password", name="test"),follow_redirects=True)
        assert response.status_code == 200

        #test with existing user username
        response = client.post('auth/register', data=dict(email="tests123@gmail.con", password="password", name=create_user.username),follow_redirects=True)
        assert response.status_code != 200

def test_register_post_invalid_email(create_user):
    with app.test_client() as client:
        #test with invalid email
        response = client.post('auth/register', data=dict(email="invalid", password="password", name="test"),follow_redirects=True)
        assert response.status_code != 200

def test_register_post_valid():
        with app.test_client() as client:
            #test with new user email and username
            response = client.post('auth/register', data=dict(email="valid@gmail.com", password="password", name="test2"),follow_redirects=True)
            assert response.status_code == 200

#test logout function
def test_logout():
    with app.test_client() as client:
        response = client.get('auth/logout')
        assert response.status_code == 302









