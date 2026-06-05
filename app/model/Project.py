from pydantic import BaseModel
from .Task import TaskRead


class Project(BaseModel):
    name: str
    description: str | None


class ProjectTask(BaseModel):
    project_name: str
    task_list: list[TaskRead]
