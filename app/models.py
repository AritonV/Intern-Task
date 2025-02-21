from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  email: str
  password: str


class Project(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str
  description: Optional[str] = None
  user_id: int


class Task(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  description: Optional[str] = None
  due_date: Optional[str] = None
  project_id: int
