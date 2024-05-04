from db import db
from app import app
from models import Question


def create_all():
    db.create_all()
    print("All tables created")


def drop_all():
    db.drop_all()
    print("All tables dropped")


def add_questions(filepath):
    with open(filepath) as file:
        # Add logic to add questions here
        pass
    db.session.commit()
    print("All questions added")


if __name__ == "__main__":
    with app.app_context():
        drop_all()
        create_all()
        add_questions("./data/questions.json")
