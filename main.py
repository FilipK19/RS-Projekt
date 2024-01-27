from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/create")
async def home(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/edit")
async def home(request: Request):
    return templates.TemplateResponse("edit.html", {"request": request})