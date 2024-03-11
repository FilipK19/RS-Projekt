from fastapi import FastAPI, Form
from pymongo import MongoClient
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["Documents"]
collection = mydb["Documents"]


# Set up CORS middleware
origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/update_document/{document_id}")
async def update_document(document_id: str, content: str = Form(...), font: str = Form(...), fsize: str = Form(...), notes: str = Form(...)):
    document_id_obj = ObjectId(document_id)
    collection.update_one({"_id": document_id_obj}, {"$set": {"content": content, "font":font, "fsize":fsize, "notes":notes}})
    return {"status": "Document updated successfully"}, 200

@app.delete("/delete/{document_id}")
async def delete_document_post(document_id: str):
    document_id_obj = ObjectId(document_id)
    result = collection.delete_one({"_id": document_id_obj})
    if result.deleted_count == 1:
        return {"status": "Document deleted successfully"}
    else:
        return {"status": "Document not found or already deleted"}