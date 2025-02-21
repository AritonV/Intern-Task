import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_user
from ..database import get_session
from ..models import Project, Task, User

router = APIRouter()


@router.post("/projects/{project_id}/tasks/", response_model=Task, tags=["tasks"])
def create_task(
    project_id: int,
    task: Task,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  project = session.get(Project, project_id)
  if not project:
    raise HTTPException(status_code=404, detail="Project not found")
  if project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to access this project")

  task.project_id = project_id
  if hasattr(task, "due_date") and task.due_date:
    task.due_date = datetime.datetime.strptime(task.due_date, "%Y-%m-%d")
  session.add(task)
  session.commit()
  session.refresh(task)
  return task


@router.get("/projects/{project_id}/tasks/", response_model=List[Task], tags=["tasks"])
def read_tasks(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  project = session.get(Project, project_id)
  if not project:
    raise HTTPException(status_code=404, detail="Project not found")
  if project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to access this project")

  tasks = session.exec(
      select(Task).where(Task.project_id == project_id)
  ).all()
  return tasks


@router.get("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def read_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  task = session.get(Task, task_id)
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")

  project = session.get(Project, task.project_id)
  if project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to access this task")

  return task


@router.put("/tasks/{task_id}", response_model=Task, tags=["tasks"])
def update_task(
    task_id: int,
    task_update: Task,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  db_task = session.get(Task, task_id)
  if not db_task:
    raise HTTPException(status_code=404, detail="Task not found")

  project = session.get(Project, db_task.project_id)
  if not project or project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to update this task")

  task_data = task_update.dict(exclude_unset=True)
  for key, value in task_data.items():
    if key == "due_date" and value:
      if value == "null":
        value = None
      else:
        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    if key != "id" and key != "project_id":
      setattr(db_task, key, value)

  session.add(db_task)
  session.commit()
  session.refresh(db_task)
  return db_task


@router.delete("/tasks/{task_id}", tags=["tasks"])
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  task = session.get(Task, task_id)
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")

  project = session.get(Project, task.project_id)
  if not project or project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to delete this task")

  session.delete(task)
  session.commit()
  return {"message": "Task deleted successfully"}
