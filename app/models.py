from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  email: str = Field(unique=True, index=True)
  password: str

  projects: List["Project"] = Relationship(back_populates="user")


class Project(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  description: str
  user_id: int = Field(foreign_key="user.id")

  user: User = Relationship(back_populates="projects")
  tasks: List["Task"] = Relationship(back_populates="project")


class Task(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  description: str
  due_date: Optional[datetime] = None
  project_id: int = Field(foreign_key="project.id")

  project: Project = Relationship(back_populates="tasks")
