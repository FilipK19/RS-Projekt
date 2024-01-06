import fastapi
from fastapi.responses import HTMLResponse


app = fastapi.FastAPI()

@app.get("/test")
async def home():
    html_content = """
    <html>
        <head>
            <title>My FastAPI App</title>
        </head>
        <body>
            <h1>Test!</h1>
            <button onclick="alert('Button Clicked!')">Click me</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)