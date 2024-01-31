from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="e_templates")

# MongoDB setup
MONGODB_URL = "mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/"
client = AsyncIOMotorClient(MONGODB_URL)
database = client["test2"]

# MongoDB document model
class DocumentModel(BaseModel):
    id: str = str(ObjectId())
    title: str
    description: str
    content: str = ""

# Routes

@app.get("/edit")
async def edit_doc(request: Request):
    documents = await get_documents()
    return templates.TemplateResponse("edit.html", {"request": request, "documents": documents})

@app.get("/edit/{document_id}")
async def edit_document(request: Request, document_id: str):
    document = await get_document(document_id)
    return templates.TemplateResponse("edit2.html", {"request": request, "document": document, "document_id": document_id})


@app.post("/edit-document/{document_id}")
async def edit_document_post(document_id: str, request: DocumentModel):
    await update_document(document_id, request.title, request.description, request.content)
    return {"message": "Document updated successfully!"}


# Helper functions
async def save_document(title: str, description: str, content: str):
    await database.documents.insert_one({"title": title, "description": description, "content": content})

async def get_documents():
    documents = await database.documents.find().to_list(length=100)
    return documents

async def get_document(document_id: str):
    document = await database.documents.find_one({"_id": ObjectId(document_id)})
    if document:
        return {"title": document["title"], "description": document["description"], "content": document["content"]}
    return None

async def update_document(document_id: str, title: str, description: str, content: str):
    await database.documents.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": {"title": title, "description": description, "content": content}}
    )
