# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Adding Trello credentials
In order to call the Trello API, you need to first create an account on https://trello.com/signup., then generate an API key and token by following the
instructions here: https://trello.com/app-key.

Once complete you need to copy the key a token from that page.

Please add a "trello.config" file in the todo_app/data folder with the following format:

[trello_auth]
key=<Trello Key>
token=<Trello Token> 

[trello_user]
user=<The Trello user>

[trello_board]
name=<The Trello board to open>


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the Tests

To run the Selenium tests, you will need to download the Gecko driver:
https://github.com/mozilla/geckodriver/releases

Place the driver at the root of the project

Before running the tests, install with pip the following:
pip install -U pytest
pip install -U mock
pip install -U requests_mock
pip install -U selenium
pip install -U selenium-requests

Troubleshooting!
Getting the driver to work can be a bit of a pain! If it isn’t working, try these things
• you’ll need the browser (FireFox in this case) installed as well as the driver.
• the browser and the driver will need to be the same version
• the driver must be on the $PATH
• on Mac, you may get a permissions error. If you do, try the steps explained here:
https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-errorchromedriver-cannot-be-opened-because-the-de