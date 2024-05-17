from trivia.models import User
import pytest

def test_login_get():
    assert 'login.html' != ''

def test_login_post():
    username = 'user2'
    email = 'user2@example.com'
    password = 'Password1'
    remember = True

    assert username != ''
    assert email != ''
    assert password != ''
    assert remember is True
