from fastapi import FastAPI, Form
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["test5"]
collection = mydb["Documents"]


# Set up CORS middleware
origins = [
    "http://127.0.0.1:8000",  # Add the origin of your frontend application
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific headers if needed
)


@app.post("/update_document/{document_id}")
async def update_document(document_id: str, content: str = Form(...)):
    document_id_obj = ObjectId(document_id)
    collection.update_one({"_id": document_id_obj}, {"$set": {"content": content}})
    return {"status": "Document updated successfully"}, 200

@app.delete("/delete/{document_id}")
async def delete_document_post(document_id: str):
    document_id_obj = ObjectId(document_id)
    result = collection.delete_one({"_id": document_id_obj})
    if result.deleted_count == 1:
        return {"status": "Document deleted successfully"}
    else:
        return {"status": "Document not found or already deleted"}