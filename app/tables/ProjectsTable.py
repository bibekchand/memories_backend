from sqlmodel import SQLModel, Field, Relationship
from .UserTable import UserTable
from .Link.ProjectTaskLink import ProjectTaskLink


class ProjectsTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = Field(default=None)
    username: str = Field(
        foreign_key="usertable.username")
    user: UserTable = Relationship(back_populates="projects")
    tasks: list["TaskTable"] = Relationship(
        back_populates="projects", link_model=ProjectTaskLink)
