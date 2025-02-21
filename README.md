# Task Management App

This is a Task Management App built with FastAPI for the backend and a simple HTML/CSS/JavaScript frontend.

## Features

- User authentication (login and registration)
- Create, edit, and delete projects
- Create, edit, and delete tasks within projects

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- SQLite (default database)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/task-management-app.git
    cd task-management-app
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
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