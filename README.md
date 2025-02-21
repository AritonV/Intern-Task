# Intern Task App

This is a Task Management App built with FastAPI for the backend and a simple HTML/CSS/JavaScript frontend.

## Features

- User authentication (login and registration)
- Create, edit, and delete projects
- Create, edit, and delete tasks within projects

## Requirements

- Python 3.10+
- FastAPI
- SQLModel
- Uvicorn
- SQLite

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/AritonV/Intern-Task.git
    cd Intern-Task
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    venv\Scripts\Activate.ps1  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the FastAPI application**:
    ```sh
    uvicorn app.main:app --reload
    ```

5. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:8000/static/index.html
    ```

## API Endpoints

- **User Authentication**:
  - `POST /api/register`: Register a new user
  - `POST /api/token`: Login and get a token

- **Projects**:
  - `GET /api/projects/`: Get all projects
  - `POST /api/projects/`: Create a new project
  - `GET /api/projects/{project_id}`: Get a specific project
  - `PUT /api/projects/{project_id}`: Update a specific project
  - `DELETE /api/projects/{project_id}`: Delete a specific project

- **Tasks**:
  - `GET /api/projects/{project_id}/tasks/`: Get all tasks for a project
  - `POST /api/projects/{project_id}/tasks/`: Create a new task in a project
  - `GET /api/tasks/{task_id}`: Get a specific task
  - `PUT /api/tasks/{task_id}`: Update a specific task
  - `DELETE /api/tasks/{task_id}`: Delete a specific task