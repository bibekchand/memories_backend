from sqlmodel import SQLModel, Field

class ProjectTaskLink(SQLModel, table=True):
    project_id: int | None = Field(
        default=None, foreign_key="projectstable.id", primary_key=True)
    task_id: int | None = Field(
        default=None, foreign_key="tasktable.id", primary_key=True)
