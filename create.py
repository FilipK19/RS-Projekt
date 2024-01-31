from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MongoDB setup
MONGODB_URL = "mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/"
client = AsyncIOMotorClient(MONGODB_URL)
database = client["test2"]  # Replace "your_database_name" with your desired database name

# MongoDB document model
class DocumentModel(BaseModel):
    id: str = str(ObjectId())
    title: str
    description: str
    content: str = ""

# Routes

@app.get("/create")
async def create_form(request: Request):
    documents = await get_documents()
    return templates.TemplateResponse("create.html", {"request": request, "documents": documents})


@app.post("/create-document/")
async def create_document(document: DocumentModel):
    await save_document(document)
    return {"message": "Document created successfully!"}


# Helper functions
async def save_document(document: DocumentModel):
    await database.documents.insert_one(document.dict())


async def get_documents():
    documents = await database.documents.find().to_list(length=100)
    return documents
