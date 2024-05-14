import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from sqlalchemy.sql import functions as func
from .db import db
from .models import Question, User
from .routes import html_bp, api_questions_bp, auth_bp

# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)


@app.context_processor
def inject_random_question_id():
    stmt = db.select(Question.id).order_by(func.random())
    random_question_id = db.session.execute(stmt).scalar()
    return dict(random_question_id=random_question_id)


app.instance_path = Path(__file__).parent.parent / "data"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.secret_key = os.getenv("SECRET_KEY")

# Initialize database
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(api_questions_bp, url_prefix="/api/questions")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/auth")
