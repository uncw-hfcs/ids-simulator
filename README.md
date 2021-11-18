# ids-simulator

## Environment Preparation

We recommend using PyCharm professional. It can be configured to automatically use the virtual environment in a terminal
and run Flask quickly.

### Windows virtual environment setup

1. Open a Command Prompt and navigate to the "crywolf" directory
2. `python -m venv .venv` -- create python virtual environment
3. `.venv\Scripts\activate` -- activates the virtual environment

### Mac/Linux virtual environment setup

1. Open a Terminal and navigate to the "crywolf" directory
2. `python3 -m venv .venv` -- create python virtual environment
3. `source .venv/bin/activate` -- activates the virtual environment

### Setup and Run

Activate the virtual environment if necessary using Step 3 from above.

1. `python -m pip install --upgrade pip setuptools wheel` -- update build tools
2. `pip install -r .\requirements.txt`
3. `flask db upgrade` -- one time command to initialize the database structure and values
4. `flask run` -- launch the flask server.
5. Browse to http://127.0.0.1:5000/