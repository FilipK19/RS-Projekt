from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()
templates = Jinja2Templates(directory="e_templates")


client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["test5"]
collection = mydb["Documents"]


@app.get("/edit", response_class=HTMLResponse)
async def create_form(request: Request):
    documents = collection.find()
    return templates.TemplateResponse("edit.html", {"request": request, "documents": documents})


@app.get("/edit_document/{document_id}", response_class=HTMLResponse)
async def edit_document(request: Request, document_id: str):
    document = get_document(document_id)
    return templates.TemplateResponse("edit2.html", {"request": request, "document": document, "document_id": document_id})


@app.post("/update_document/{document_id}")
async def update_document(document_id: str, content: str = Form(...)):
    document_id_obj = ObjectId(document_id)
    collection.update_one({"_id": document_id_obj}, {"$set": {"content": content}})
    return {"status": "Document updated successfully"}



def get_document(document_id: str):
    document = collection.find_one({"_id": ObjectId(document_id)})
    if document:
        return {"name": document["name"], "description": document["description"], "content": document["content"]}
    return None