import pytest
from trivia.models import Question, Quiz, QuizQuestion, User


@pytest.fixture
def user():
    # Basic user fixture
    user = User(username="drai_29", email="dleon@oilers.ca", password="gooilersgo")
    return user


def test_new_user(user):
    # Check attributes and password hashing (pass/fail)
    user = User(username="Lethamyr", email="leth@psyonix.com", password="rokt_l33g")
    assert user.role == "user"
    assert user.username == "Lethamyr"
    assert user.email == "leth@psyonix.com"
    assert user.password_hashed != "rokt_l33g"
