from sqlmodel import SQLModel, Field, Relationship
from .UserTable import UserTable
from .Link.ProjectTaskLink import ProjectTaskLink
from ..enums.TaskStatus import TaskStatus


class TaskTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = Field(default=None)
    username: str = Field(foreign_key="usertable.username")
    date: str | None = Field(default=None)
    time: str | None = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.pending)
    user: UserTable = Relationship(back_populates="tasks")
    projects: list["ProjectsTable"] = Relationship(
        back_populates="tasks", link_model=ProjectTaskLink)
