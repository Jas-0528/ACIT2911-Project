import pytest
from trivia.routes import auth
from trivia import app

#create user for testing
@pytest.fixture
def create_user():
    with app.app_context():
        user = auth.User(username="test", email="testing@gmail.com", password="password")
        return user
    
#test if the user is created
def test_new_user(create_user):
    assert create_user.username == "test"
    assert create_user.email == "testing@gmail.com"

#test auth.register function -> check if the register page is rendered
def test_register_page():
    with app.test_client() as client:
        response = client.get('auth/register')
        assert response.status_code == 200
    
#test auth.login function -> check if the login page is rendered
def test_login_page():
    with app.test_client() as client:
        response = client.get('auth/login')
        assert response.status_code == 200

#test if register_post function redirects to login page if user is created
def test_register_post():
    with app.app_context():
        with app.test_client() as client:
            response = client.post('auth/register', data=dict(username="test", email="testing@gmail.com", password="password"))
            assert response.status_code == 302
                                                

#test if register_post function redirects to register page if email already exists
def test_register_post_existing_email(create_user):
    with app.test_client() as client:
        #response will be a redirect to register page
        response = client.post('auth/register', data=dict(email="testing@gmail.com", password="password", username="test"))
        assert response.status_code == 302



