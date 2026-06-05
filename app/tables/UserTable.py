from sqlmodel import SQLModel, Field, Relationship



class UserTable(SQLModel, table=True):
    username: str = Field(primary_key=True)
    password: str = Field(min_length=8)
    email: str
    projects: list["ProjectsTable"] = Relationship(back_populates="user")
    tasks: list["TaskTable"] = Relationship(back_populates="user")
