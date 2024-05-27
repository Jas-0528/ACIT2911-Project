## __Init__.py
The init.py file runs functions to do the following tasks:  
- initializes the database for the application
- create the flask application
- load environmental variables

This is done to start up crucial elements to run the application.


## Manage.py
The manage.py file is used to manage the database of the application by
- Fetching trivia questions from the Trivia Question API and makes them a JSON file.
- Creating test users and test quizzes for testing. 
- When running the file itself, the __name__ == "main" block will delete and create data as a refresh.


## Db.py
The db.py file essentially allows for interaction with the database of questions for the Trivia application. Through SQLAlchemy and Flask, the database is called through functions which allow it to be represented by the variable "db" for easy use in other python files.