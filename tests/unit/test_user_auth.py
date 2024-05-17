import pytest
from trivia.routes import auth
from trivia import app


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

#create user for testing
@pytest.fixture
def create_user():
    with app.app_context():
        user = auth.User(username="test", email="testing@gmail.com", password="password")
        return user
    
#test if the user is registered successfully
def test_register(create_user):
    assert create_user.username == "test"
    assert create_user.email == "testing@gmail.com"
    #test if the password is hashed
    assert create_user.password_hashed != "password"

#test if user is logged in successfully
def test_register_post():
    with app.app_context():
        with app.test_client() as client:
            response = client.post('auth/register', data=dict(username="test", email="testing@gmail.com", password="password"))
            assert response.status_code == 302
                                                

#test if user is not registered if email or username  already exists
def test_register_post_existing_user(create_user):
    with app.test_client() as client:
        #response will be a redirect to register page
        response = client.post('auth/register', data=dict(email="testing@gmail.com", password="password", username="test123"))
        assert response.status_code == 302



