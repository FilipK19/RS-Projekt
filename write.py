from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="w_templates")



@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})