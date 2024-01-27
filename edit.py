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

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/edit")
async def edit_doc(request: Request):
    documents = get_documents()
    return templates.TemplateResponse("edit.html", {"request": request, "documents": documents})


def get_documents():
    db = SessionLocal()
    documents = db.query(DocumentModel).all()
    db.close()
    return documents
