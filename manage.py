from db import db
from app import app
from models import Question
import json
import requests
import html

def convert_to_json():
    # Make API request to OpenTDB
    url = "https://opentdb.com/api.php?amount=50&type=multiple" 
    response = requests.get(url)
    data = response.json()["results"]
    print("Converted to JSON")

    # write out the gotten data to a file
    with open("data/trivia.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Written to file")

# create database tables
def create_all():
    db.create_all()
    print("All tables created")

# drop all tables
def drop_all():
    db.drop_all()
    print("All tables dropped")

# add questions to the database from json file created from the API
def add_questions():
    # read the questions.json file
    with open("data/trivia.json") as file:
        # Add logic to add questions here
        data = json.load(file)
        
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
        drop_all()
        create_all()
        convert_to_json()
        add_questions()