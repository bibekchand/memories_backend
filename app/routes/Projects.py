from fastapi import APIRouter, Depends, HTTPException
from ..model.Project import Project
from ..db_config import SessionDep
from ..settings import get_settings
from ..dependencies import verify_token
from fastapi.security import OAuth2PasswordBearer
from ..tables.ProjectsTable import ProjectsTable
from ..tables.TaskTable import TaskTable
from ..tables.UserTable import UserTable
from ..model.Task import TaskAdd
from ..model.Project import ProjectTask
from ..model.Task import TaskRead
from typing import Annotated

router = APIRouter(tags=["Projects"])

auth = OAuth2PasswordBearer(tokenUrl="login")

settings = get_settings()


@router.post("/projects")
def add_projects(token: Annotated[str, Depends(auth)], session: SessionDep, project: Project):
    username = verify_token(token, session)
    db_task = ProjectsTable(
        name=project.name, description=project.description, username=username)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/projects")
def get_user_projects(token: Annotated[str, Depends(auth)], session: SessionDep):
    username = verify_token(token, session)
    user = session.get(UserTable, username)
    return user.projects


@router.get("/projects/tasks", response_model=ProjectTask)
def get_project_tasks(token: Annotated[str, Depends(auth)], session: SessionDep, project_id: int):
    project = session.get(ProjectsTable, project_id)
    return {"project_name": project.name, "task_list": project.tasks}


@router.delete("/projects")
def delete_project(token: Annotated[str, Depends(auth)], session: SessionDep, id):
    project = session.get(ProjectsTable, id)
    if not project:
        raise HTTPException(status_code=404,
                            detail="Project not found")
    session.delete(project)
    session.commit()
    return project


@router.post("/projects/task/{project_id}", response_model=TaskRead)
def add_task_to_project(project_id: int, token: Annotated[str, Depends(auth)], session: SessionDep, task: TaskAdd):
    project = session.get(ProjectsTable, project_id)
    username = verify_token(token, session)
    if not project:
        raise HTTPException(status_code=404,
                            detail="Project not found")
    task_db = TaskTable(title=task.title, description=task.description,
                        username=username, date=task.date, time=task.time, status=task.status)
    project.tasks.append(task_db)
    session.commit()
    session.refresh(project)
    return task_db
