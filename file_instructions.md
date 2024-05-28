<!-- AN: This shouldn't be in the root directory and should be named more semantically. -->
<!-- AN: Is this the user-targeted or dev-targeted doc? If it is the user-targeted one, add instructions to clone the repository -->

<!-- AF: will send this over to philip's branch -->

# Trivia Game File Structure and Guide

 <!-- AN: Consider renaming this heading "Trivia Game File Structure and Guide" or something similarly more meaningful... like the filename. -->
 <!-- AF: Done! -->

Welcome to the file structure instructions for understanding your Trivia Game website. Follow these steps to get started!

## Launching the Game

<!-- AN: Not sure where you're planning to include it but instructions for creating a venv and installing packages from requirements.txt is crucial -->

1. **Open Terminal** <!-- AN: Any terminal can be used, not just Terminal -->: Open your terminal and navigate to your project directory.

2. **Run the Manage Script**: Enter the command `python manage.py` to set up your environment. <!-- AN: Please mention and describe the options/flags, including -h. manage.py does not set up the environment. python/py/python3 -m venv <venv_directory_name> does. Please also mention that. -->

3. **Start the Server**: Run the command `py ./app` or `python app.py`. <!-- AN: python app.py is more common. Please also use python, py or python3 consistently --> This will start the server and display a link.

4. **Access the Game**: You can access the game in one of three ways: - Follow the link displayed in the terminal to access the Trivia Game (http://127.0.0.1:8888) - Enter localhost:8888 in the address bar (search bar located at the top of the browser) - Paste **127.0.0.1:8888** to your address bar

<!-- AN: The primary instruction should be to open a web browser and enter localhost:<PORT> or 127.0.0.1:<PORT>. Information on which port should also be provided. -->
<!-- AF: Done! -->
<!-- AN: Information on which port should also be provided. -->
<!-- AN: Please explain the generate_env_file.py script and its options/flags. -->
<!-- AF: philip should have that on his file -->
<!-- AN: This should be in the user docs (as well) -->

## HTML Templates

**The HTML templates are located**:

```
C:\
└── trivia
    └── templates
        └── <file-name>.html
```

<!--  AN: Only C:\ if you put it there! Should be the project root -->

<!-- AN: These are all templates, not pages! Explain when the templates are used and their content/variables, and maybe the routes that interact with them, not the pages themselves. -->

**Login Page**: When the website is run, users will be taken to the login page (`login.html`).

**Registration Page**: If a user needs to register, they can follow the link to the registration page (`register.html`).

**Home Page**: After logging in or registering, users are directed to the home page (`home.html`).

**Playing a Game**: Users can choose to play a quiz or resume a quiz from the home page. They can also select random mode from the navigation bar.

**Game Page**: Based on their selection, users are taken to the game page (`play.html`) to start answering questions.

**After Quiz**: After completing or leaving a quiz, users are taken back to the home page (`home.html`).

## base.html (trivia > templates > base.html) <!-- AN: These should be under the Templates section above -->

Contains the navigation bar markup. The navigation bar is present on all website pages, including **Home**, **Play Quiz**, **Play Random**, **Log In**, **Register**

## login.html (trivia > templates > login.html) <!-- AN: These should be under the Templates section above -->

- Contains the login page layout. <!-- AN: Not really a list and it is inconsistent with the base.html section above. -->
- Includes inputs for entering in a _username_, _email_, _password_, a _"Remember me"_ checkbox, a link to the registration page ("Don't have an account? Register here"), and flash messages. <!-- AN: check grammar. -->

## register.html (trivia > templates > register.html) <!-- AN: These should be under the Templates section above -->

- Contains the registration page layout.
- Includes inputs for username, email, password, and a register button.

## home.html (trivia > templates > home.html) <!-- AN: These should be under the Templates section above -->

Displays the home page after a user logs in.
It includes buttons and dropdowns for: <!-- AN: Mention the conditional. There is also a Delete Quiz button sometimes. Jas will also make a Play Random button; please mention that. -->

- "Play Random" and "Play Quiz" can be selected from the navigation bar.
- "Play Random"
- "Play Quiz"
- "Resume Quiz"
- Category selection
- Difficulty selection
- Length of quiz
- Delete Quiz— only present when you have a saved quiz
- Conditional messages
  > The home page appearance varies based on whether a quiz needs to be resumed or not.

### play.html (trivia > templates > play.html)

- Displays the game page.
- Includes elements for:
  - Scoreboard
  - Question card
  - Answer options
  - Result of the question (correct or incorrect feedback)
  - One of the following will be displayed depending on the quiz mode:
    1.  Random question button
    2.  Next question arrow

## app.py (located in root) <!-- Use heading levels to organize all files in a structure similar to the project structure: root, data, trivia, tests, etc. -->

`app.py` serves as the main application code. It defines routes, handles requests, and is in charge the application's functionality.
Our `app,py` <!-- AN: app.py --> runs a development server on local host (`port = 8888`) to test the application. <!-- AN: not always 8888 -->

## models.py (located in root)

`models.py` is responsible for handling the database operations. It utilizes SQLAlchemy, which allows SQL statements to be mapped to relational database operations using Python objects. <!-- AN: Check Philip's breakdown. I like his detailed approach and description. Agree on something. -->

### Conditionals <!-- This information can be put into individual templates' sections, but not really necessary. It definitely shouldn't be a subheading of models.py -->

Conditionals are statements that perform different
actions based on specified conditions. There are many conditionals throughout the game.

For one, the scoreboard appears differently between the _Play Quiz_ and _Play Random_ game modes. Play Quiz shows a users score, question category, the current question they're on, and the difficulty. Play Random does **not** show the users score.

On both quiz modes, the answer options are white with a pink border, but when a question is answered, all the answer options are greyed out.

If the question is answered correctly--you click the right answer--the "Correct!" message will appear in green coloured text. If the answer you choose is wrong, a "Sorry, the answer was `<correct answer>`" will appear.

<!-- AN: Describe the relationships and the class methods -->

<!-- AN: General notes: -->
<!-- AN: Rework the headings. They could be organized like the actual directory structure (root, trivia, tests, data...) -->
