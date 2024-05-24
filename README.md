# Trivia Game Website Instructions

Welcome to the Trivia Game website! Follow these steps to start playing:

## Creating an Account

1. **Register**: Go to the login page and create an account by entering your email, username, and password.
2. **Log In**: Use your new credentials to sign in.

## Home Page

After logging in, you'll be directed to the home page. Here, you'll see three buttons:

1. **Category**: Choose the category of questions you want to answer. You can also select "all" to get questions from every category.
2. **Difficulty**: Select the difficulty level (easy, medium, hard). You can also choose "all" for a mix of difficulties.
3. **Number of Questions**: Decide how many questions you want to answer.

## Playing the Quiz

- **Scoring**: You earn points based on the difficulty of the questions:
  - Easy: 1 point
  - Medium: 2 points
  - Hard: 3 points

- **Scoreboard**: While playing, the scoreboard displays:
  - Your current score
  - The category of the question
  - The current question number out of the total (e.g., Question 3 out of 5)
  - The difficulty of the current question

- **Answering Questions**:
  - When you answer a question correctly, "Correct!" appears.
  - If you answer incorrectly, "Sorry, the answer is [correct answer]" is displayed.
  - An arrow appears at the bottom to move to the next question.
 
-**Saving and Resuming Progress**:

- You can leave the quiz at any time, and your progress will be saved.
- To resume, click on the “Resume Quiz” button on the home page.

## Deleting a Quiz

- You can delete a quiz by returning to the home page and clicking the "Delete Quiz" button.

## Playing Random Mode

- **Play Random**: Select this mode to get questions from all categories and difficulties.
  - In this mode, the specific category and difficulty of each question are displayed.
  - Note: Scores are not tracked in random mode.

- **Next Random Question**: Click on the “Random Question” button to generate a new question.


# Trivia Game Website - Backend Instructions


Welcome to the backend instructions for setting up and running your Trivia Game website. Follow these steps to get started:


## Launching the Game


1. **Open Python Terminal**: Open your terminal and navigate to your project directory.
2. **Run the Manage Script**: Enter the command `python manage.py` to set up your environment.
3. **Start the Server**: Run the command `py ./app`. This will start the server and display a link in the terminal.
4. **Access the Game**: Follow the link displayed in the terminal to access theTrivia Game.


## HTML Templates


### User Flow


1. **Login Page**: When the website is first run, users will be taken to the login page (`login.html`).
2. **Registration Page**: If a user needs to register, they can follow the link to the registration page (`register.html`).
3. **Home Page**: After logging in or registering, users are directed to the home page (`home.html`).
4. **Playing a Game**: Users can choose to play a quiz or resume a quiz from the home page. They can also select random mode from the navigation bar.
5. **Game Page**: Based on their selection, users are taken to the game page (`play.html`) to start answering questions.
6. **After Quiz**: After completing or leaving a quiz, users are taken back to the home page (`home.html`).




### 1. base.html


- Contains the navigation bar markup.
- The navigation bar is present on all website pages, including Home, Play Quiz, Play Random, Log In, and Log Out.


### 2. login.html


- Contains the login page layout.
- Includes inputs for entering email, password, a "Remember me" checkbox, and a link to the registration page ("Don't have an account? Register here").


### 3. register.html


- Contains the registration page layout.
- Includes inputs for username, email, password, and a register button.


### 4. home.html


- Displays the home page after a user logs in.
- Includes buttons and dropdowns for:
  - "Play Quiz"
  - "Resume Quiz"
  - Category selection
  - Difficulty selection
  - Length of quiz
- Users can also select "Random Mode" from the navigation bar.


### 5. play.html


- Displays the game page.
- Includes elements for:
  - Scoreboard
  - Question card
  - Answer options
  - Result of the question (correct or incorrect feedback)
  - One of the following will be displayed depending on the quiz mode:
    1.  Random question button
    2. Next question arrow



## App.py

The `app.py` file defines the game and runs it locally on `localhost` on port `8888`.

## Models.py

`models.py` is responsible for handling the database operations. It utilizes SQLAlchemy, which allows SQL statements to be mapped to relational database operations using Python objects.

> Questions were taken from Open Trivia DB API (https://opentdb.com/api_config.php)