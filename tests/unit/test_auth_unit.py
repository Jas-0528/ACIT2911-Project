from flask import url_for
from trivia.db import db
from trivia.models import User


# Test if user is in the database
def test_user_in_db(db_user):
    stmt = db.select(User).where(User.username == db_user.username)
    result = db.session.execute(stmt)
    user = result.scalars().first()
    assert user is not None
    assert user.username == db_user.username


# Test auth.login function -> check if the login page is rendered
def test_login_page(client):
    response = client.get(url_for("auth.login"))
    assert response.status_code == 200


# Test auth.register function -> check if the register page is rendered
def test_register_page(client):
    response = client.get(url_for("auth.register"))
    assert response.status_code == 200
