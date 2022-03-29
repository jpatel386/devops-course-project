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

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

Once copied, find and add in the values for your trello api. You will need the trello key, token and board id. 

To make sure this works, you will need to have python-dotenv installed to automatically detect the .env file.

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

## Running the tests

Make sure you have run poetry install. pytest is an included dependency so will get installed. 

The integrations have a dependency on chrome driver being present. 

Navigate to the todo_app directory, i.e. directly above the tests directory. You can now run the tests by executing:
```bash
$ poetry run pytest tests/
```

## Using a VM
You can use Vagrant to run the app. To o so, make sure you have vagrant installed. Then run the following:
```bash
$ vagrant up
```

## Using Docker
You can use Docker to run the app
Build an image using the Dockerfile included by running the following command
```
docker build --tag todo-app .
```
Once you have an image, you can run it in a container using the command
```
docker run -d -p 0.0.0.0:5000:5000 --env-file .env todo-app --mount type=bind,source="($pwd)",target=/app 
```
Note this is port 5000 in gunicorn too which is changed from the default of 80

## TODO

Document DOCKER in prod/dev envs

## Documentation of the Application

Documentation can be found in the documentation folder at the root level of this repo

To build a test image of the docker, run the following to build the image
```
docker build --target test --tag my-test-image .
```
To run the image for UNIT and INTEGRATION tests, execute the following
```
docker run --env-file .env.test my-test-image todo_app/tests
```
To run the image for e2e tests, execute the following
```
docker run --env-file .env my-test-image todo_app/e2e_tests
```

##Updating paths to ignore on github workflows
If you add files which when committed or pushed do not need to trigger a github action, then add them to the workflow file under the paths_ignore section.

##Extra notes
If you are running this on an M1 Mac, check the notes.txt as it contains useful info about running the app



