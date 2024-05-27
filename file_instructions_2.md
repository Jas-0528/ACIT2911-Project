<!-- A: Include a title/heading 1 and rename the file to match. I'm not really sure what the purpose of this file is. -->
<!-- A: put this in the appropriate dir. -->

## **Init**.py <!-- A: Should not be capitalized. Some OSes are case sensitive. -->

The init.py <!-- A: Missing underscores --> file runs functions to do the following tasks:

- initializes the database for the application
- create the flask application
- load environmental variables
  <!-- A: This does a lot more. Check the file and its comments. -->
  <!-- A: Mention the location of this file. There are more than one and can be more. -->

This is done to start up crucial elements to run the application.

## Manage.py <!-- A: Should not be capitalized. Some OSes are case sensitive. -->

The manage.py file is used to manage the database of the application by <!-- A: Describe this as a script. Missing colon. -->

- Fetching trivia questions from the Trivia Question API and makes them a JSON file. <!-- A: Check grammar. -->
- Creating test users and test quizzes for testing. 
- When running the file itself, the **name** == "main" block will delete and create data as a refresh.

## Db.py <!-- A: Should not be capitalized. Some OSes are case sensitive. -->

The db.py file essentially allows for interaction with the database of questions for the Trivia application. Through SQLAlchemy and Flask, the database is called through functions which allow it to be represented by the variable "db" for easy use in other python files.

<!-- A: General notes: -->
<!-- Keep your lists and grammar consistent. They are not parallel right now. -->