# Trivia Game User Guide

This guide provides instructions on how to set up and run the Trivia Game application locally.

## Cloning the Repository

The repository can be cloned from GitHub using either HTTPS or SSH. Cloning using HTTPS requires your GitHub credentials to be entered every time code is pushed to the repository. Cloning using SSH allows interaction with the repository without the need for credentials each time, but requires set up SSH keys.

### Cloning Using HTTPS

Clone the repository using HTTPS:

```bash
git clone https://github.com/Jas-0528/ACIT2911-Project.git path/to/repository
```

Replace `path/to/repository` with the path where you want the cloned repository to be located on your local machine.

### Cloning Using SSH

Cloning via SSH requires a pair of SSH keys to be set up between your local system and a GitHub account. GitHub provides information on generating SSH keys [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and adding them [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

After SSH keys have been set up, clone the repository:

```bash
git clone git@github.com:Jas-0528/ACIT2911-Project.git path/to/repository
```

Replace `path/to/repository` with the path where you want the cloned repository to be located on your local machine.

## Setting Up a Virtual Environment

A virtual environment is recommended when using the application. Using a virtual environment isolates the application and its dependencies from the global Python environment on your system, reducing the risk of version conflicts and making it easier to manage the project's dependencies.

Setting up a virtual environment and running the application require Python and pip to be installed on your local system. Follow instructions on the official Python website [here](https://www.python.org) or those provided by your operating system's package manager to install Python and pip.

After the repository has been cloned, navigate to the project directory and create a virtual environment:

```bash
python -m venv .venv
```

`.venv` represents the name of virtual environment directory and can be replaced with other common names such as `venv` or `env`.

After the virtual environment is created, activate it:

- on Linux or macOS:

```bash
source .venv/bin/activate
```

- on Windows:

```powershell
.venv/Scripts/Activate
```

The virtual environment should be active every time a command related to the application is run to ensure that the dependencies specific to the project are used, and to prevent conflicts.

## Installing Required Packages

Install packages required by the application (dependencies):

```bash
pip install -r requirements.txt
```

This will install all the packages listed in the `requirements.txt` file.

## Using Utility Scripts

### Managing the Database with `manage.py`

By default, the `manage.py` management script:

- drops all tables in the SQLite database
- recreates all tables (empty)
- adds questions to the database from JSON file
- creates and adds test accounts

Run the script:

```bash
python manage.py
```

The following flags can be used with the command:

- `-h` or `--help`: Show a help message and exit. This will display information about these flags.

- `-w` or `--write-to-json`: Write 50 new trivia questions from the [Open Trivia Database](https://opentdb.com/) to a JSON file in the `data` directory (by default, named `trivia.db`).

- `-a` or `--append-to-json`: Append a specified number of batches of 50 trivia questions each from the [Open Trivia Database](https://opentdb.com/) to an existing JSON file in the `data` directory (by default, named `trivia.db`). The number of batches is specified as an argument to the flag.

- `-q` or `create-random-quiz`: Create a random quiz for a random user in the database. The quiz consists of 1 to 4 random questions from the database.

#### Creating a Test Database

It is good practice to run tests (located in the `tests` directory) using a test database to not affect the primary/production database. The `pytest.ini` file contains an environment variable which ensures that a test database is used when tests are run with pytest.

Create a test database:

- on Linux or macOS:

```bash
TESTING=1 python manage.py
```

- on Windows:

```powershell
$env:TESTING = "1"; python manage.py; Remove-Item Env:\TESTING
```

The same flags can be used when using the management script like this.

### Generating a Local .env File with `generate_env_file.py`

This `generate_env_file.py` script generates a .env file with a secret key and a port number. The secret key is a random 64-character hexadecimal string required by Flask-login. The port number defaults to 8888, and another port can be specified using a flag.

The following flags can be used with the command:

- `-h` or `--help`: Show a help message and exit. This will display information about these flags.

- `p` or `--port`: Specify a port number as an argument to the flag. Without this flag, the port written defaults to 8888.

## Running the Application Locally

Ensure that the following have been completed before running the application:

- Python and pip are installed
- [a virtual environment has been set up and is active](#setting-up-a-virtual-environment)
- [the required packages are installed](#installing-required-packages)
- [an SQLite database has been created and populated with questions using the management script](#creating-and-populating-the-database)
- [a local .env file has been created](#creating-a-local-env-file)

Run the application:

```bash
python app.py
```

Trivia Game will then be accessible at localhost:8888 or 127.0.0.1:8888. If you specified a different port number in the .env file, use that instead. For example, localhost:\<port> or 127.0.0.1:\<port>.

Instructions to register, log in and play the game are in the [README](../README.md).
