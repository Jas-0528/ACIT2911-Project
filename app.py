import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from pathlib import Path
from db import db
from models import User
from routes import html_bp, api_questions_bp, auth_bp

# Load the environment variables from the .env file
load_dotenv()

# Create Flask application
app = Flask(__name__)

app.instance_path = Path("./data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.secret_key = os.getenv("SECRET_KEY")

# Initialize the database with the app
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(api_questions_bp, url_prefix="/api/questions")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/auth")


if __name__ == "__main__":
    app.run(debug=True, port=80)
