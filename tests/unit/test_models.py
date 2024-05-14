from trivia.models import User


def test_new_user():
    user = User(username="user2", email="user2@example.com", password="password1")
    assert user.role == "user"
    assert user.username == "user2"
    assert user.email == "user2@example.com"
    assert user.password_hashed != "password1"
