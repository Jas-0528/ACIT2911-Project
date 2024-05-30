<!-- AN: This shouldn't be in the root directory and should be named more semantically. -->
<!-- AN: Is this the user-targeted or dev-targeted doc? If it is the user-targeted one, add instructions to clone the repository -->

<!-- AF: will send this over to philip's branch -->

# Trivia Game File Structure and Guide

 <!-- AN: Consider renaming this heading "Trivia Game File Structure and Guide" or something similarly more meaningful... like the filename. -->
 <!-- AF: Done! -->

Welcome to the file structure instructions for understanding your Trivia Game website. Follow these steps to get started!

## Launching the Game

<!-- AN: Not sure where you're planning to include it but instructions for creating a venv and installing packages from requirements.txt is crucial -->
<!-- AF: added that as a sub-heading (Creating a virtual env) -->

1. **Open Terminal**: 
Open your terminal and navigate to your project directory.

2. **Run the Manage Script**: Enter the command `python manage.py` to set up your environment.
 <!-- AN: Please mention and describe the options/flags, including -h. manage.py does not set up the environment. python/py/python3 -m venv <venv_directory_name> does. Please also mention that. -->

3. **Start the Server**: Run the command `py ./app` or `python app.py`. This will start the server and display a link.
  
4. **Access the Game**: You can access the game in one of four ways: 
- Enter the URL (`triviagame.xyz`)
- Follow the link displayed in the terminal to access the Trivia Game (http://127.0.0.1:8888) 
- Enter **localhost:<`port`>** in the address bar (search bar located at the top of the browser) 
- Paste **127.0.0.1:8888** to your address bar

**Creating a Virtual Environment:**
1. Open Command Prompt.
2. Navigate to your project folder using `cd your_project_folder`.
3. Create a virtual environment: `python -m venv myenv`.
4. Activate it: On Windows, `myenv\Scripts\activate`; on Mac/Linux, `source myenv/bin/activate`.
5. Install packages: `pip install -r requirements.txt`. 

_Remember to replace your_project_folder and myenv with your actual folder and desired environment name._

<!-- AN: The primary instruction should be to open a web browser and enter localhost:<PORT> or 127.0.0.1:<PORT>. Information on which port should also be provided. -->
<!-- AF: Done! -->
<!-- AN: Information on which port should also be provided. -->
<!-- AN: Please explain the generate_env_file.py script and its options/flags. -->
<!-- AF: philip should have that on his file -->
<!-- AN: This should be in the user docs (as well) -->

# HTML Templates

**The HTML templates are located**:

```
root
└── trivia
    └── templates
        └── <file-name>.html
```

<!--  AN: Only C:\ if you put it there! Should be the project root -->

<!-- AN: These are all templates, not pages! Explain when the templates are used and their content/variables, and maybe the routes that interact with them, not the pages themselves. -->

## Login Page (trivia > templates > login.html): 
This page is displayed when a user wants to log in.  Contains the login page layout. It also includes inputs for entering in a _username_, _email_, _password_, a _"Remember me"_ checkbox, a link to the registration page ("Don't have an account? Register here"), and flash messages.

## Registration Page
When a new user wants to register, they can follow the _"Don't have an account? Register here"_ link--from the login page--to get to the registration page. This template Contains the registration page layout and includes inputs for username, email, password, and a register button. These inputs are required!

## Home Page (trivia > templates > home.html):

After logging in or registering, users are directed to the home page.
This page is for the homepage. The contents of this page includes:
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

**Playing a Game**: Users can choose to play a quiz or resume a quiz from the home page. They can also select random mode from the navigation bar.

**Game Page**: Based on their selection, users are taken to the game page to start answering questions.

**After Quiz**: After completing or leaving a quiz, users are taken back to the home page.

## base.html (trivia > templates > base.html)
Contains the navigation bar markup. The navigation bar is present on all website pages, including **Home**, **Play Quiz**, **Play Random**, **Log In**, and **Register**


## play.html (trivia > templates > play.html)

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
```
root
    └── app.py
```

`app.py` serves as the main application code. It defines routes, handles requests, and is in charge the application's functionality.
Our `app.py` runs a development server on local host to test the application. 
<!-- AN: not always 8888 -->
<!-- AF: I removed that line---(Port=8888) -->



## Conditionals <!-- This information can be put into individual templates' sections, but not really necessary. It definitely shouldn't be a subheading of models.py -->
<!-- AF: Made it into its own heading.  -->

Conditionals are statements that perform different
actions based on specified conditions. There are many conditionals throughout the game.

For one, the scoreboard appears differently between the _Play Quiz_ and _Play Random_ game modes. Play Quiz shows a users score, question category, the current question they're on, and the difficulty. Play Random does **not** show the users score.

On both quiz modes, the answer options are white with a pink border, but when a question is answered, all the answer options are greyed out.

If the question is answered correctly--you click the right answer--the "Correct!" message will appear in green coloured text. If the answer you choose is wrong, a "Sorry, the answer was `<correct answer>`" will appear.

<!-- AN: Describe the relationships and the class methods -->
<!-- AF: You said philip did this 😝-->

<!-- AN: General notes: -->
<!-- AN: Rework the headings. They could be organized like the actual directory structure (root, trivia, tests, data...) -->
