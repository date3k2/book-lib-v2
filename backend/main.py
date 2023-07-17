from fastapi import Cookie, FastAPI, Query, Body, Path, Form, File, UploadFile, Depends
from pydantic import BaseModel
from typing import Annotated
from uuid import UUID, uuid1
from datetime import datetime, time, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

class Student2(BaseModel):
    grade: int


class Student(Student2):
    name: str
    age: int
    description: str | None = None


class Item(BaseModel):
    id: int
    tags: list[str]


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# generate a random secret key for the application

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/time/")
async def time():
    return {"time": datetime.now().date()}


@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[int, Depends(oauth2_scheme)]):
    return {"item_id": item_id}


@app.post("/items/", status_code=201)
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
async def create_student(student: Student) -> Student2:
    return student


@app.post("/login/", description="Login to the application", tags=["Login"])
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@app.put("/items2/")
async def update_item(
    item: Annotated[Item, Body()],
    item_id: Annotated[
        int,
        Cookie(),
    ] = None,
):
    return {"item_id": item_id, "item": item}


@app.post(
    "/uploadfile/",
    description="API tải lên file và trả về tên file",
    summary="Post file",
)
async def create_upload_file(file: UploadFile = File()):
    return {"filename": file.filename}


# command for running the server
# uvicorn main:app --reload

# Make the server reload on code changes and log all the requests
# uvicorn main:app --reload --log-level debug
