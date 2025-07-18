import uvicorn
from fastapi import FastAPI, Path, Body, Request, Form, Cookie
from typing import List
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = []
class Book(BaseModel):
   id: int
   title: str
   author: str
   publisher: str

class Student(BaseModel):
    id : int
    name : str = Field(None, title="name of student", max_length=10)
    subject: List[str] = []

class User(BaseModel):
    username: str
    password: str


@app.post("/book")
def add_book(book: Book):
   data.append(book.dict())
   return data

@app.get("/list")
def get_books():
   return data

@app.get("/book/{id}")
def get_book(id: int):
   id = id - 1
   return data[id]

@app.put("/book/{id}")
def add_book(id: int, book: Book):
   data[id-1] = book
   return data

@app.delete("/book/{id}")
def delete_book(id: int):
   data.pop(id-1)
   return data

@app.post("/cookie/")
def create_cookie():
    content = {"message" : "cookie_set"}
    response = JSONResponse(content=content)
    response.set_cookie(key="usrname", value="admin")
    return response

@app.get("/readcookie/")
async def read_cookie(usrname: str = Cookie(None)):
    return { "username": usrname }




@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", { "request": request })

@app.post("/submit/", response_model=User)
async def submit(nm: str = Form(...), pwd: str = Form(...)):
    return User(username=nm, password=pwd)

@app.post("/students")
async def student_data(name:str=Body(...), marks:int=Body(...)):
    return { "name": name, "marks": marks}


@app.get("/history/", response_class=HTMLResponse)
async def history(request: Request):
    return templates.TemplateResponse("history.html", { "request": request })

@app.get("/logo/{name}", response_class=HTMLResponse)
async def logo(request: Request, name: str):
    return templates.TemplateResponse("logo.html", {"request": request, "name": name})


@app.get("/")
async def index():
    return {'message': "Hello World!"}

@app.get("/hello/{name}/{age}")
async def hello(*, name:str=Path(..., min_length=3, max_length=10), age:int=Path(..., ge=1, le=100 )):
    return { "name": name, "age": age }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)