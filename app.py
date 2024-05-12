from flask import Flask
from pathlib import Path
from db import db
from routes import (
    html_bp,
    api_questions_bp,
    auth_bp
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trivia.db"
app.instance_path = Path("./data").resolve()

db.init_app(app)

app.register_blueprint(api_questions_bp, url_prefix="/api/questions")
app.register_blueprint(html_bp, url_prefix="/")
app.register_blueprint(auth_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True, port=8019)
