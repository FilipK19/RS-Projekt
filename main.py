import fastapi
import requests
import time


app = fastapi.FastAPI()



@app.get("/")
async def home():

    return {
        "Status": "OK"
    }