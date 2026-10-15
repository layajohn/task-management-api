# Task Management REST API

This is a simple task management API I built using Python, Flask, and SQLite. It lets users create tasks, view them, update their details, and delete them.

I built this project to get more hands-on practice with backend development, working with databases, and testing API endpoints.

## What it can do

- View all tasks
- Create a new task
- View a specific task using its ID
- Update an existing task
- Delete a task
- Check for missing task titles and invalid status values
- Return appropriate responses when a task doesn't exist
- Run automated tests using pytest

## Technologies used

- Python
- Flask
- SQLite
- pytest
- Git and GitHub

## Getting started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd task-management-api
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository's URL once you've created it on GitHub.

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the required packages

```bash
python3 -m pip install -r requirements.txt
```

### 4. Start the API

```bash
python3 app.py
```

The application should run locally at `http://127.0.0.1:5000`.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the API home page |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/<task_id>` | Get a task by ID |
| PUT | `/tasks/<task_id>` | Update a task |
| DELETE | `/tasks/<task_id>` | Delete a task |

## Running the tests

To run the tests, use:

```bash
python3 -m pytest -v
```

The project currently has 9 tests covering the main operations, including creating, retrieving, updating, and deleting tasks, along with a few invalid-request cases.

## Project structure

```text
task-management-api/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_app.py
```

## Possible improvements

- Add user registration and login
- Add task priorities and due dates
- Add options to filter and paginate tasks
- Improve the API documentation
- Add more tests for invalid requests and errors