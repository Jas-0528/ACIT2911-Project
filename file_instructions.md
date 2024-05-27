<!-- A: This shouldn't be in the root directory and should be named more semantically. -->
<!-- A: Is this the user-targeted or dev-targeted doc? If it is the user-targeted one, add instructions to clone the repository -->

# Trivia Game Website - Backend Instructions <!-- A: Consider renaming this heading "Trivia Game File Structure and Guide" or something similarly more meaningful... like the filename. -->
# Trivia Game Website - Backend Instructions (HTML Files)

Welcome to the backend instructions for understanding your Trivia Game website. Follow these steps to get started!

Welcome to the backend instructions <!-- A: Backend instructions don't really mean anything and the content as of this comment aren't really instructions --> for setting up and running your Trivia Game website. Follow these steps to get started:

## Launching the Game

1. **Open Terminal** <!-- A: Terminal? You can use any terminal. -->: Open your terminal and navigate to your project directory.
2. **Run the Manage Script**: Enter the command `python manage.py` to set up your environment. <!-- A: Please mention and describe the options/flags, including -h. manage.py does not set up the environment. python/py/python3 -m venv <venv_directory_name> does. Please also mention that. -->
3. **Start the Server**: Run the command `py ./app`. <!-- A: python app.py is more common. Please also use python, py or python3 consistently --> This will start the server and display a link in the terminal.
4. **Access the Game**: Follow the link displayed in the terminal to access theTrivia Game.
<!-- A: The primary instruction should be to open a web browser and enter localhost:<PORT> or 127.0.0.1:<PORT>. Information on which port should also be provided.>

<!-- A: Please explain the generate_env_file.py script and its options/flags. -->
> You can also enter in the webiste's URL (http://127.0.0.1:8888)

## HTML Templates

<!-- A: Arrows aren't necessary. This is not how templates work. They are rendered by route functions, but the user is never "taken" to any HTML template. Please explain when each template is used and the variables they each might use. Explain the role of base.html -->

➔ **Login Page**: When the website is run, users will be taken to the login page (`login.html`).

➔ **Registration Page**: If a user needs to register, they can follow the link to the registration page (`register.html`).

➔ **Home Page**: After logging in or registering, users are directed to the home page (`home.html`).

➔ **Playing a Game**: Users can choose to play a quiz or resume a quiz from the home page. They can also select random mode from the navigation bar.

➔ **Game Page**: Based on their selection, users are taken to the game page (`play.html`) to start answering questions.

➔ **After Quiz**: After completing or leaving a quiz, users are taken back to the home page (`home.html`).

### 1. base.html

<!-- A: These are not steps. They should not be numbered. -->

- Contains the navigation bar markup.
- The navigation bar is present on all website pages, including Home, Play Quiz, Play Random, Log In, Log Out, and flash messsages. <!-- A: The navbar is not present in flash messages and there is not Log Out page. It is present on the Register page as well. -->

### 2. login.html

- Contains the login page layout.
- Includes inputs for entering <!-- A: Username. Please also check order. --> email, password, a "Remember me" checkbox, a link to the registration page ("Don't have an account? Register here"), and flash messages.

### 3. register.html

- Contains the registration page layout.
- Includes inputs for username, email, password, and a register button.

### 4. home.html

- Displays the home page after a user logs in.
- Includes buttons and dropdowns for: <!-- A: Mention the conditional. There is also a Delete Quiz button sometimes. Jas will also make a Play Random button; please mention that. -->
  - "Play Quiz"
  - "Resume Quiz"
  - Category selection
  - Difficulty selection
  - Length of quiz
- Users can also select "Random Mode" from the navigation bar. <!-- It's not "Random Mode" but we can change that if we want. -->
- Users can also select "Random Mode" from the navigation bar.

> The home page appearance varies based on whether a quiz needs to be resumed or not.


### 5. play.html

<!-- a: Mention/describe conditionals -->

- Displays the game page.
- Includes elements for:
  - Scoreboard
  - Question card
  - Answer options
  - Result of the question (correct or incorrect feedback)
  - One of the following will be displayed depending on the quiz mode:
    1.  Random question button
    2.  Next question arrow

## App.py <!-- A: Should not be capitalized. Some OSes are case sensitive. -->

<!-- pending--haven't revised it after comment -->

The `app.py` file defines the game and runs it locally on `localhost` on port `8888`.
## App.py
`app.py` serves as the main application code. It defines routes, handles requests, and is in charge the application's functionality. 
Our `app,py` runs a development server on local host (`port = 8888`) to test the application.


## Models.py

`models.py` is responsible for handling the database operations. It utilizes SQLAlchemy, which allows SQL statements to be mapped to relational database operations using Python objects.

<!-- A: Describe the relationships and the class methods -->

> Questions were taken from Open Trivia DB API (https://opentdb.com/api_config.php) <!-- A: Why is this under Models.py? Move it to the README -->

<!-- A: General notes: -->
<!-- A: Rework the headings. They could be organized like the actual directory structure (root, trivia, tests, data...) -->
