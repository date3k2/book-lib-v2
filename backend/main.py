from fastapi import Cookie, FastAPI, Query, Body, Path
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID, uuid1
from datetime import datetime, time, timedelta


class Student(BaseModel):
    name: str
    age: int
    grade: int
    description: str | None = None


class Item(BaseModel):
    id: int
    tags: list[str]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/time/")
async def time():
    return {"time": datetime.now().date()}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.post("/items/")
async def create_item(
    name: Annotated[str, Body()],
    description: Annotated[
        str, Body(max_length=5, title="Create item for project", alias="dsc")
    ] = None,
):
    if description:
        return {"name": name, "description": description, "id": uuid1()}
    return {"name": name, "id": uuid1()}


@app.post("/students/")
async def create_student(student: Student):
    return student


@app.put("/items2/")
async def update_item(
    item: Annotated[Item, Body()],
    item_id: Annotated[
        int,
        Cookie(),
    ] = None,
):
    return {"item_id": item_id, "item": item}


# command for running the server
# uvicorn main:app --reload

# Make the server reload on code changes and log all the requests
# uvicorn main:app --reload --log-level debug
