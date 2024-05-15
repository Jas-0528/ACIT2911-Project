from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from trivia.db import db
from trivia.models import User

auth_bp = Blueprint("auth", __name__)


# Login page
@auth_bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


# Login post
@auth_bp.route("/login", methods=["POST"])
def login_post():
    # Get form data email and password or name
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    login_method = request.form.get("login_method")

    # Search database for matching username or email to login_method

    stmt = select(User).where(User.email == login_method)
    result = db.session.execute(stmt)
    user = result.scalars().first()
    if not user:
        stmt = select(User).where(User.username == login_method)
        result = db.session.execute(stmt)
        user = result.scalars().first()
    if not user or not check_password_hash(user.password_hashed, password):
        flash("User not found: check login details")
        return redirect(url_for("auth.login"))

    # If user is found, log them in
    login_user(user, remember=remember)
    # If login is successful, redirect to homepage
    return redirect(url_for("html.home"))


# Register page
@auth_bp.route("/register", methods=["GET"])
def register():
    return render_template("register.html")


# Register post
@auth_bp.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("name")

    # Check if user already exists
    stmt = select(User).where(User.email == email)
    result = db.session.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        flash("Email address already exists")
        return redirect(url_for("auth.register"))

    # Else create new user and hash password
    new_user = User(
        email=email,
        username=username,
        password=password,
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


# Logout page
@auth_bp.route("/logout", methods=["GET"])
def logout():
    return "You have been logged out"
