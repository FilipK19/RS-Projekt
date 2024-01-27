from fastapi import FastAPI, Request, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from docx import Document
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="c_templates")


# SQLite database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/create")
async def create_form(request: Request):
    documents = get_documents()
    return templates.TemplateResponse("create.html", {"request": request, "documents": documents})


@app.post("/create-document/")
async def create_document(title: str = Form(...), description: str = Form(...)):
    save_document(title, description)
    return {"message": "Document created successfully!"}



# Helper functions
def save_document(title: str, description: str):
    db = SessionLocal()
    db_document = DocumentModel(title=title, description=description)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    db.close()

def get_documents():
    db = SessionLocal()
    documents = db.query(DocumentModel).all()
    db.close()
    return documents
