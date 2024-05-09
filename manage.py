from db import db
from app import app
from models import Question
import json
import requests
import html


def write_to_json():
    # Make API request to OpenTDB
    url = "https://opentdb.com/api.php?amount=50&type=multiple"
    response = requests.get(url)
    data = response.json()["results"]
    print("Converted to JSON")

    # Write out JSON to file
    with open("data/trivia.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
    print("Written to file")


def append_to_json():
    # Make API request to OpenTDB
    url = "https://opentdb.com/api.php?amount=50&type=multiple"
    response = requests.get(url)
    data = response.json()["results"]
    print("Converted to JSON")

    # Read existing data
    try:
        with open("data/trivia.json", "r") as infile:
            existing_data = json.load(infile)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    # Append new data
    existing_data.extend(question for question in data if question not in existing_data)

    # Write out JSON to file
    with open("data/trivia.json", "w") as outfile:
        json.dump(existing_data, outfile, indent=4)
    print("Appended to file")


# Create database tables
def create_all():
    db.create_all()
    print("All tables created")


# Drop database tables
def drop_all():
    db.drop_all()
    print("All tables dropped")


# Add questions to the database from json file created from the API
def add_questions():
    # Read the trivia.json file
    with open("data/trivia.json") as file:
        data = json.load(file)

    # Loop though each question and add it to the database
    for question in data:
        new_question = Question(
            question=html.unescape(question["question"]),
            correct_answer=html.unescape(question["correct_answer"]),
            incorrect_answers=[
                html.unescape(answer) for answer in question["incorrect_answers"]
            ],
            category=html.unescape(question["category"]),
            difficulty=html.unescape(question["difficulty"]),
        )
        # Add the question to the database
        db.session.add(new_question)

    # Once all questions have been added, commit the transaction
    db.session.commit()
    print("All questions added")


if __name__ == "__main__":
    with app.app_context():
        # write_to_json()
        # append_to_json()
        drop_all()
        create_all()
        add_questions()
