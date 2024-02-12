from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient


app = FastAPI()
templates = Jinja2Templates(directory="templates")



client = MongoClient('mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/')
db = client['Userdata']
collection = db['users']



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register_user/")
async def register_user(name: str = Form(...), password: str = Form(...)):

    if collection.find_one({"name": name}):
        raise HTTPException(status_code=400, detail="Username already registered")

    user_data = {"name": name, "password":password}
    collection.insert_one(user_data)

    return {"status": "User registered successfully"}