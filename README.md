# Trivia Game Website Instructions <!-- A: "Website" Instructions? Consider just using "Trivia Game" or "Trivia Game Web Application"? -->

Welcome to the Trivia Game website! Follow these steps to start playing: <!-- A: Steps? What steps? -->

## Creating an Account

<!-- A: Do you need an account to play? -->

1. **Register**: Go to the login page and create an account by entering your email, username, and password. <!-- A: You cannot create an account on the login page. Also need a step telling them to sit some button. Also consider telling them the password requirements. -->
2. **Log In**: Use your new credentials to sign in. <!-- A: Logging in should be its own section. -->

## Home Page

After logging in, you'll be directed to the home page. Here, you'll see three drop downs: <!-- A: drop-down/dropdown list/menu, not "drop down" -->

<!-- A: Jas will also add a Play Random button to the homepage. Please mention this. -->

1. **Category**: Choose the category of questions you want to answer. You can also select "all" to get questions from every category.
2. **Difficulty**: Select the difficulty level (easy, medium, hard). You can also choose "all" for a mix of difficulties.
3. **Number of Questions**: Decide how many questions you want to answer.

#### Click on the "Play Quiz" button to start your game!

## Playing Quiz Mode

<!-- A: You're defeating the purpose of markdown by using HTML and all the functionality HTML markup you're using can be replicated with markdown. Let me know if you need help. -->
<!-- A: How do you start Quiz mode? Why isn't there a button at the top like Play Random? Is Quiz Mode endless? What IS quiz mode? Imagine explaining this to someone new. -->
<h3 style="display: inline;">Scoring:</h3> <!-- A: Headings should be on their own line, no colon -->
<h4 style="display: inline; font-weight: normal;">You earn points based on the difficulty of the questions:</h4>  <!-- A: Headings should be on their own line, no colon -->
  <li><span style="font-weight: bold;">Easy:</span> 1 point</li>
  <li><span style="font-weight: bold;">Medium:</span> 2 points</li>
  <li><span style="font-weight: bold;">Hard:</span> 3 points</li>

<br>
<br>

<h3 style="display: inline;">Scoreboard:</h3>  <!-- A: Headings should be on their own line, no colon -->
<h4 style="display: inline; font-weight: normal">While playing, the scoreboard displays:</h4>  <!-- A: Headings should be on their own line, no colon -->
<ul>
  <li>Your current score</li>
  <li>The category of the question</li>
  <li>The current question number out of the total (e.g., Question 3 out of 5)</li>
  <li>The difficulty of the current question</li>
</ul>
 
<h3>Saving and Resuming Progress:</h3>  <!-- A: Headings should not have a colon -->
<li>You can leave the quiz at any time, and your progress will be saved.
<li>To resume, click on the “Resume Quiz” button on the home page.

<h3>Deleting a Quiz</h3>
<li>You can delete a quiz by returning to the home page and clicking the "Delete Quiz" button. <!-- A: What does it mean to delete a quiz? (Consider telling the user that each logged in account can have one saved quiz at a time, which is created on the homepage) -->

## Playing Random Mode <!-- A: Consider moving this above ## Playing Quiz Mode -->

- **Play Random**: Select this mode to get questions from all categories and difficulties. <!-- A: What is the point of this line? You could probably have a heading here or remove it entirely -->
  - In this mode, the specific category and difficulty of each question are displayed.
  - Note: Scores are not tracked in random mode.

<!-- A: How do you play Random Mode? How many questions do you get to play? Can you play this mode while there is a Quiz? Imagine explaining this to someone new. -->

- **Next Random Question**: Click on the “Random Question” button to generate a new question. <!-- A: This doesn't need to be a bullet point -->

<br><br> <!-- A: What's this HTML for? -->

<!-- A: General notes: -->
<!-- A: You're overusing bullet points. Bullet points are used for unnumbered lists. Numbered lists are useful for steps, but otherwise, still to plain paragraphs. -->
