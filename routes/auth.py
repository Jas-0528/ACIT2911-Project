import random
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy.sql import functions as func
from db import db
from models import Question, User
from werkzeug.security import generate_password_hash
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login():
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("login.html", random_id=random_id)

@auth_bp.route("/register", methods=["GET"])
def register():
    random_id = db.session.query(Question.id).order_by(func.random()).first()[0]
    return render_template("signup.html", random_id=random_id)

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