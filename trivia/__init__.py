import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import current_user, LoginManager
from pathlib import Path
from sqlalchemy.sql import functions as func
from .db import db
from .models import Question, Quiz, User
from .routes import html_bp, api_bp, auth_bp

# Load environment variables from .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)


# Supply each template with a random question id for Play Random link
@app.context_processor
def inject_data():
    # Get a random question id
    stmt = db.select(Question.id).order_by(func.random())
    random_question_id = db.session.execute(stmt).scalar()

    # Check if a Quiz exists
    if current_user.is_authenticated:
        stmt = db.select(Quiz).where(Quiz.user_id == current_user.id)
        quiz = db.session.execute(stmt).scalar()
    else:
        quiz = None

    return dict(random_question_id=random_question_id, quiz_exists=bool(quiz))


app.instance_path = (Path(__file__).parent.parent / "data").resolve()
if os.getenv("TESTING"):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_trivia.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"

# Retrieve secret key
secret_key = os.getenv("SECRET_KEY")
if secret_key is None:
    raise ValueError("No SECRET_KEY set for Flask application")
app.secret_key = secret_key

# Initialize database
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


app.register_blueprint(api_bp, url_prefix="/api/questions")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/auth")
