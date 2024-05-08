from db import db
from app import app
from models import Question
import json
import requests
import html

#create the json file
def json_file():
    # Make an API request to OpenTDB (replace with the correct endpoint and parameters)
    url = "https://opentdb.com/api.php?amount=50&type=multiple"  #  Get 50 questions
    response = requests.get(url)
    data = response.json()
    print(data)
    # Now you have both database questions and API questions in the "output.json" file

    # write out the gotten data to a file
    with open("questions.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

# create database tables
def create_all():
    db.create_all()
    print("All tables created")

# drop all tables
def drop_all():
    db.drop_all()
    print("All tables dropped")

# add questions to the database
def add_questions(filepath):
    # read the questions.json file
    with open(filepath) as file:
        # Add logic to add questions here
        data = json.load(file)
        data = data["results"]
    #loop though each question and add it to the database
    for question in data:
        new_question = Question(
            question=html.unescape(question["question"]),
            correct_answer=html.unescape(question["correct_answer"]),
            incorrect_answers=[html.unescape(answer) for answer in question["incorrect_answers"]],
            category=html.unescape(question["category"]),
            difficulty=html.unescape(question["difficulty"]),
        )
        # add the question to the database
        db.session.add(new_question)
    # once all questions have been added, commit the transaction
    db.session.commit()
    print("All questions added")


if __name__ == "__main__":
    with app.app_context():
        json_file()
        drop_all()
        create_all()
        add_questions("./questions.json")