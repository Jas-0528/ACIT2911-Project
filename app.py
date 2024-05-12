from flask import Flask
from pathlib import Path
from db import db
from routes import (
    html_bp,
    api_questions_bp,
    auth_bp
)
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.secret_key = "super-secret"
app.instance_path = Path("./data").resolve()

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(api_questions_bp, url_prefix="/api/questions")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/auth")

        


if __name__ == "__main__":
    app.run(debug=True, port=8019)
