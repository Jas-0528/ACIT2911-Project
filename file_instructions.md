
# Trivia Game Website - Backend Instructions


Welcome to the backend instructions for setting up and running your Trivia Game website. Follow these steps to get started:


## Launching the Game


1. **Open Terminal**: Open your terminal and navigate to your project directory.
2. **Run the Manage Script**: Enter the command `python manage.py` to set up your environment.
3. **Start the Server**: Run the command `py ./app`. This will start the server and display a link in the terminal.
4. **Access the Game**: Follow the link displayed in the terminal to access theTrivia Game.


## HTML Templates
➔ **Login Page**: When the website is run, users will be taken to the login page (`login.html`).

➔ **Registration Page**: If a user needs to register, they can follow the link to the registration page (`register.html`).

➔ **Home Page**: After logging in or registering, users are directed to the home page (`home.html`).

➔ **Playing a Game**: Users can choose to play a quiz or resume a quiz from the home page. They can also select random mode from the navigation bar.

➔ **Game Page**: Based on their selection, users are taken to the game page (`play.html`) to start answering questions.

➔ **After Quiz**: After completing or leaving a quiz, users are taken back to the home page (`home.html`).






### 1. base.html


- Contains the navigation bar markup.
- The navigation bar is present on all website pages, including Home, Play Quiz, Play Random, Log In, Log Out, and flash messsages.


### 2. login.html


- Contains the login page layout.
- Includes inputs for entering email, password, a "Remember me" checkbox, a link to the registration page ("Don't have an account? Register here"), and flash messages.


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
<!-- pending--haven't revised it after comment -->
The `app.py` file defines the game and runs it locally on `localhost` on port `8888`.

## Models.py

`models.py` is responsible for handling the database operations. It utilizes SQLAlchemy, which allows SQL statements to be mapped to relational database operations using Python objects.

> Questions were taken from Open Trivia DB API (https://opentdb.com/api_config.php)