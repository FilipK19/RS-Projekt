from fastapi import FastAPI, Form
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["test5"]
collection = mydb["Documents"]


@app.post("/create_document/")
async def create_document(name: str = Form(...), description: str = Form(...), content: str = Form(default='')):
    document = {"name": name, "description": description, "content": content}
    collection.insert_one(document)
    return {"status": "Document created successfully"}, 200