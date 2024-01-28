from fastapi import FastAPI, Request, Form
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from docx import Document
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="e_templates")


# SQLite database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    content = Text

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/edit")
async def edit_doc(request: Request):
    documents = get_documents()
    return templates.TemplateResponse("edit.html", {"request": request, "documents": documents})

@app.get("/edit/{document_id}")
async def edit_document(request: Request, document_id: int):
    document = get_document(document_id)
    return templates.TemplateResponse("edit2.html", {"request": request, "document": document})

@app.post("/edit-document/{document_id}")
async def edit_document_post(document_id: int, title: str = Form(...), description: str = Form(...), content: str = " "):
    update_document(document_id, title, description, content)
    return {"message": "Document updated successfully!"}

# Helper functions
def save_document(title: str, description: str, content: str):
    db = SessionLocal()
    db_document = DocumentModel(title=title, description=description, content=content)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    db.close()

def get_documents():
    db = SessionLocal()
    documents = db.query(DocumentModel).all()
    db.close()
    return documents

def get_document(document_id: int):
    db = SessionLocal()
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    db.close()
    return document

def update_document(document_id: int, title: str, description: str ,content: str):
    db = SessionLocal()
    db_document = db.query(DocumentModel).filter(DocumentModel.id == document_id).first()
    db_document.title = title
    db_document.description = description
    db_document.content = content
    db.commit()
    db.refresh(db_document)
    db.close()
