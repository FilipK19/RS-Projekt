import fastapi
from fastapi.responses import HTMLResponse


app = fastapi.FastAPI()



@app.get("/")
async def home():
    html_content = """
    <html>
        <head>
            <title>My FastAPI App</title>
             <style>
                body {
                    text-align: center;
                    margin: 20px;
                }
                h1 {
                    color: #333;
                }
                p {
                    color: #666;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to my FastAPI App!</h1>
            <p>This is some additional text.</p>
             <a href="/test">
                <button>Go to Another Page</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/test")
async def home():
    html_content = """
    <html>
        <head>
            <title>Test</title>
        </head>
        <body>
            <h1>Test!</h1>
             <a href="/">
                <button>Back</button>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)