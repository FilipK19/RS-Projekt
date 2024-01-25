import fastapi
from fastapi.responses import HTMLResponse


app = fastapi.FastAPI()

@app.get("/create")
async def home():
    html_content = """
    <html>
        <head>
            <title>Test</title>
            <style>
                body {
                    text-align: center;
                    margin: 20px;
                }
                h1 {
                    margin: 5px 0;
                    font-family: "Book Antiqua", Palatino, serif;
                    font-size: 65px;
                }
                .input-container {
                    margin-top: 50px;
                }
                textarea {
                    width: 65%;
                    height: 750px;
                    margin: 10px;
                    font-size: 16px;
                    box-sizing: border-box;
                    resize: vertical;
                }
            </style>
        </head>
        <body>
            <h1>Collaborate</h1>
            <div class="input-container">
                <textarea id="textField"></textarea>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)