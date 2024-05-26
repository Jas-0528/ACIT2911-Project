import re
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from trivia.db import db
from trivia.models import User

auth_bp = Blueprint("auth", __name__)


# Login page
@auth_bp.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("html.home"))
    return render_template("login.html")


# Login post
@auth_bp.route("/login", methods=["POST"])
def login_post():
    if current_user.is_authenticated:
        return redirect(url_for("html.home"))
    # Get form data email and password or username
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    login_method = request.form.get("login_method")

    # Search database for matching username or email to login_method
    stmt = db.select(User).where(User.email == login_method)
    result = db.session.execute(stmt)
    user = result.scalars().first()

    # If no user found with matching email, find user with matching username
    if not user:
        stmt = db.select(User).where(User.username == login_method)
        result = db.session.execute(stmt)
        user = result.scalars().first()

    # If no user found, redirect to login page and flash no user found
    if not user:
        flash("No user found with that email or username")
        return redirect(url_for("auth.login"))
    # If user is found, check password
    if not check_password_hash(user.password_hashed, password):
        flash("Incorrect password, try again")
        return redirect(url_for("auth.login"))

    # If user is found, log them in
    login_user(user, remember=remember)
    # If login is successful, redirect to homepage
    return redirect(url_for("html.home"))


# Register page
@auth_bp.route("/register", methods=["GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("html.home"))
    return render_template("register.html")


# Register post
@auth_bp.route("/register", methods=["POST"])
def register_post():
    if current_user.is_authenticated:
        return redirect(url_for("html.home"))

    # Get form data
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    # Check that all fields have input
    if not email or not username or not password:
        flash("All fields are required")
        return redirect(url_for("auth.register"))

    # Check if password meets criteria
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$", password):
        flash(
            "Password must contain at least one uppercase letter, one lowercase letter, one number, and be at least 8 characters long"
        )
        return redirect(url_for("auth.register"))

    # Check if user email already exists
    stmt = db.select(User).where(User.email == email)
    result = db.session.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        flash("Email address already in use")
        return redirect(url_for("auth.register"))

    # Check if username already exists
    stmt = db.select(User).where(User.username == username)
    result = db.session.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        flash("Username already exists")
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
    # Log user out
    logout_user()
    return redirect(url_for("auth.login"))
