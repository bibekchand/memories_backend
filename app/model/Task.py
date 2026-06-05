from pydantic import BaseModel
from sqlmodel import Field
from ..enums.TaskStatus import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: str | None = Field(default=None)
    date: str
    time: str
    status: TaskStatus


class TaskRead(TaskBase):
    id: int


class TaskAdd(TaskBase):
    projects: list[int] | None = Field(default=None)
