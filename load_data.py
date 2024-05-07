from app import app, db
from models import Question  # Assuming you have a Question model
import requests
import json


# Retrieve trivia questions from the database
# with app.app_context():
#     questions = Question.query.all()

# Save questions to a JSON file


# Make an API request to OpenTDB (replace with the correct endpoint and parameters)
url = "https://opentdb.com/api.php?amount=10"  # Example: Get 10 questions
response = requests.get(url)
data = response.json()
print(data)
# Now you have both database questions and API questions in the "output.json" file

with open("output.json", "w") as outfile:
     json.dump(data, outfile, indent=4)