from fastapi import APIRouter, Depends
from ..dependencies import verify_token
from fastapi.security import OAuth2PasswordBearer
from ..db_config import SessionDep
from typing import Annotated
from ..tables.TaskTable import TaskTable
from ..tables.ProjectsTable import ProjectsTable
from ..model.SearchResult import SearchResult
from sqlmodel import select, or_

router = APIRouter(tags=["Search"])


@router.get("/search/{query}", response_model=SearchResult)
def search(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="login"))], session: SessionDep, query: str):
    username = verify_token(token, session)
    statement = select(ProjectsTable).where(ProjectsTable.username == username, or_(ProjectsTable.name.contains(query), ProjectsTable.description.contains(query)))
    projects = session.exec(statement)
    statement = select(TaskTable).where(TaskTable.username == username, or_(TaskTable.title.contains(query), TaskTable.description.contains(query)))
    tasks = session.exec(statement)
    projects = projects.all()
    tasks = tasks.all()
    return SearchResult(projects=[p.model_dump() for p in projects], tasks=[t.model_dump() for t in tasks])
