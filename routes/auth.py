import random
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.sql import functions as func
from db import db
from models import Question, User
from werkzeug.security import generate_password_hash, check_password_hash
auth_bp = Blueprint("auth", __name__)
from flask_login import login_user

#render the login page
@auth_bp.route("/login", methods=["GET"])
def login():
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("login.html", random_id=random_id)

@auth_bp.route("/login", methods=["POST"])
def login_post():
    # get the form data email and password or name
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    login_method = request.form.get("login_method")
    #search database for matching username or email to login_method
    user = User.query.filter_by(email=login_method).first()
    if not user:
        user = User.query.filter_by(username=login_method).first()
    if not user or not check_password_hash(user.password, password):
        flash("User not found: check login details")
        return redirect(url_for("auth.login"))

    #if user is found, log them in
    login_user(user, remember=remember)
    #if login is successful, redirect to the home page
    return redirect(url_for("html.home"))

#render the register page
@auth_bp.route("/register", methods=["GET"])
def register():
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("signup.html", random_id=random_id)

#take the form data and create a new user
@auth_bp.route("/register", methods=["POST"])
def register_post():
    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("name")

    #check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash("Email address already exists")
        return redirect(url_for("auth.register"))
    
    #else create new user and hash password
    new_user = User(email=email, username=username, password=generate_password_hash(password, method="pbkdf2:sha256"))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))

@auth_bp.route("/logout", methods=["GET"])
def logout():
    return("You have been logged out")