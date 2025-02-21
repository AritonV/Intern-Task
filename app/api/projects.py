from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..auth import get_current_user
from ..database import get_session
from ..models import Project, User

router = APIRouter()


@router.post("/projects/", response_model=Project, tags=["projects"])
def create_project(
    project: Project,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  project.user_id = current_user.id
  session.add(project)
  session.commit()
  session.refresh(project)
  return project


@router.get("/projects/", response_model=List[Project], tags=["projects"])
def read_projects(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  projects = session.exec(
      select(Project).where(Project.user_id == current_user.id)
  ).all()
  return projects


@router.get("/projects/{project_id}", response_model=Project, tags=["projects"])
def read_project(
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
  return project


@router.put("/projects/{project_id}", response_model=Project, tags=["projects"])
def update_project(
    project_id: int,
    project_update: Project,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  db_project = session.get(Project, project_id)
  if not db_project:
    raise HTTPException(status_code=404, detail="Project not found")
  if db_project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to update this project")

  project_data = project_update.dict(exclude_unset=True)
  for key, value in project_data.items():
    if key != "id" and key != "user_id":
      setattr(db_project, key, value)

  session.add(db_project)
  session.commit()
  session.refresh(db_project)
  return db_project


@router.delete("/projects/{project_id}", tags=["projects"])
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
  project = session.get(Project, project_id)
  if not project:
    raise HTTPException(status_code=404, detail="Project not found")
  if project.user_id != current_user.id:
    raise HTTPException(
      status_code=403, detail="Not authorized to delete this project")

  session.delete(project)
  session.commit()
  return {"message": "Project deleted successfully"}
