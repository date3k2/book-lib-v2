from fastapi import FastAPI, Query, Body, Path
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID, uuid1


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


@app.put("/items/{item_id}}")
async def update_item(
    item_id: Annotated[int, Path()], item: Annotated[Item, Body(embed=False)]
):
    results = {"item_id": item_id, "item": item}
    return results


# command for running the server
# uvicorn main:app --reload

# Make the server reload on code changes and log all the requests
# uvicorn main:app --reload --log-level debug
