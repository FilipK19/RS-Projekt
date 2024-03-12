from fastapi import FastAPI, Form
from pymongo import MongoClient
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


@app.post("/create_document/")
async def create_document(name: str = Form(...), description: str = Form(...), 
                          content: str = Form(default=''), font: str = Form(default='Calibri'), 
                          fsize: str = Form(default='12px'), notes: str = Form(default=' '), creator: str = Form(...)):
    document = {"name": name, "description": description, "content": content, "font":font, "fsize":fsize, "notes":notes, "creator":creator}
    collection.insert_one(document)
    return {"status": "Document created successfully"}, 200