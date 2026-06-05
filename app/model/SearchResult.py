from pydantic import BaseModel
from .Task import TaskRead

class ProjectRead(BaseModel):
    id: int
    name: str

class SearchResult(BaseModel):
    projects: list[ProjectRead]
    tasks: list[TaskRead]