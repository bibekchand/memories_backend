from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from ..db_config import SessionDep
from fastapi.security import OAuth2PasswordBearer
from ..dependencies import verify_token
from ..model.Task import TaskRead, TaskAdd
from ..tables.ProjectsTable import ProjectsTable
from ..tables.TaskTable import TaskTable
from ..tables.UserTable import UserTable

router = APIRouter(tags=["Task"])

auth = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/task")
def add_task(token: Annotated[str, Depends(auth)], session: SessionDep, task: TaskAdd):
    username = verify_token(token, session)
    project_list = []
    for project_id in task.projects:
        project = session.get(ProjectsTable, project_id)
        if not project:
            continue
        project_list.append(project)
    task = TaskTable(title=task.title, description=task.description,
                     username=username, date=task.date, time=task.time, status=task.status, projects=project_list)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"message": "Task added successfully"}


@router.get("/task", response_model=list[TaskRead])
def get_user_task(token: Annotated[str, Depends(auth)], session: SessionDep):
    username = verify_token(token, session)
    user = session.get(UserTable, username)
    return user.tasks

@router.get("/task/pending/count")
def get_pending_task_count(token: Annotated[str, Depends(auth)], session: SessionDep):
    username = verify_token(token, session)
    user = session.get(UserTable, username)
    return {"count": len([task for task in user.tasks if task.status == "pending"])}

@router.delete("/task/{task_id}", response_model=TaskRead)
def delete_task(task_id: int, token: Annotated[str, Depends(auth)], session: SessionDep):
    verify_token(token, session)
    task = session.get(TaskTable, task_id)
    if task:
        session.delete(task)
        session.commit()
        return task 
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/task/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task: TaskAdd, token: Annotated[str, Depends(auth)], session: SessionDep):
    verify_token(token, session)
    task_db = session.get(TaskTable, task_id)
    if task_db:
        task_db.title = task.title
        task_db.description = task.description
        task_db.date = task.date
        task_db.time = task.time
        task_db.status = task.status
        project_list = task_db.projects
        for project_id in task.projects:
            project = session.get(ProjectsTable, project_id)
            project_list.append(project)
        task_db.projects = project_list
        session.commit()
        session.refresh(task_db)
        return task_db
    else:
        raise HTTPException(status_code=404, detail="Task not found")