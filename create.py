from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient


app = FastAPI()
templates = Jinja2Templates(directory="templates")


client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["test5"]
collection = mydb["Documents"]



@app.get("/create", response_class=HTMLResponse)
async def create_form(request: Request):
    documents = collection.find()
    return templates.TemplateResponse("create.html", {"request": request, "documents": documents})


@app.post("/create_document/")
async def create_document(name: str = Form(...), description: str = Form(...), content: str = Form(default='')):
    document = {"name": name, "description": description, "content": content}
    collection.insert_one(document)
    return {"status": "Document created successfully"}