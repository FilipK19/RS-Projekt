from fastapi import FastAPI, Form
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

client = MongoClient("mongodb+srv://admin:admin123@cluster0.1cbo1.mongodb.net/")
mydb = client["test5"]
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


@app.post("/create_document/")
async def create_document(name: str = Form(...), description: str = Form(...), content: str = Form(default='')):
    document = {"name": name, "description": description, "content": content}
    collection.insert_one(document)
    return {"status": "Document created successfully"}, 200